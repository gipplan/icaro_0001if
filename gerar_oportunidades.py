import os
import json
import re
import urllib.parse
import requests
from google import genai
from google.genai import types

# Tenta carregar a biblioteca de busca de imagens como segunda opção
try:
    from duckduckgo_search import DDGS
    DDG_DISPONIVEL = True
except ImportError:
    DDG_DISPONIVEL = False

# Fallback final estável do ecossistema iFood caso todas as tentativas falhem
IMAGEM_FALLBACK_DEFAULT = "https://images.unsplash.com/photo-1526367790999-0150786686a2?w=800&q=80"

def carregar_playbook():
    """Carrega as diretrizes estratégicas de PR do iFood."""
    try:
        with open('playbook.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Nenhum playbook personalizado encontrado. Siga as diretrizes de Diretor Sênior de PR do iFood."

def validar_ou_gerar_link(link_original, titulo_noticia):
    """
    Testa se o link da notícia retornado pela API responde com status de sucesso.
    Caso esteja quebrado, gera um fallback com busca direta no Google.
    """
    if link_original and link_original.startswith("http"):
        try:
            res = requests.head(link_original, timeout=2, allow_redirects=True)
            if res.status_code < 400:
                return link_original
        except Exception:
            pass
            
    query = urllib.parse.quote(f"{titulo_noticia} iFood")
    return f"https://www.google.com/search?q={query}"

def obter_imagem_valida(imagem_original, categoria="institucional"):
    """
    Lógica de imagens em 2 etapas:
    1ª Opção: Testa e usa a imagem retornada pela notícia original.
    2ª Opção: Faz busca por imagens do termo 'iFood' + categoria.
    Fallback: Utiliza imagem genérica de entrega/tecnologia.
    """
    # --- OPÇÃO 1: Validar imagem capturada da notícia ---
    if imagem_original and imagem_original.startswith("http"):
        try:
            res = requests.head(imagem_original, timeout=2, allow_redirects=True)
            tipo_conteudo = res.headers.get("content-type", "").lower()
            if res.status_code < 400 and ("image" in tipo_conteudo or "jpg" in imagem_original or "png" in imagem_original):
                return imagem_original
        except Exception:
            pass

    # --- OPÇÃO 2: Busca por imagem com termo 'iFood' ---
    if DDG_DISPONIVEL:
        try:
            termo_busca = f"iFood {categoria} brasil"
            with DDGS() as ddgs:
                resultados = list(ddgs.images(termo_busca, max_results=1))
                if resultados and "image" in resultados[0]:
                    return resultados[0]["image"]
        except Exception as e:
            print(f"⚠️ Aviso na busca secundária de imagem: {e}")

    # --- FALLBACK FINAL ---
    return IMAGEM_FALLBACK_DEFAULT

def gerar_oportunidades():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave da API não encontrada nas variáveis de ambiente.")
    
    # Suporte a buscas personalizadas enviadas via GitHub Actions / busca.html
    marca_alvo = os.environ.get("MARCA_ALVO", "").strip()
    
    client = genai.Client(api_key=api_key)
    
    print("🔍 Diagnosticando modelos disponíveis para a sua chave de API...")
    try:
        modelos_disponiveis = [m.name for m in client.models.list() if "gemini" in m.name]
        print(f"Modelos encontrados: {modelos_disponiveis}")
    except Exception as e:
        print(f"Aviso: Não foi possível listar os modelos. Erro: {e}")
    
    playbook_texto = carregar_playbook()

    # Define o escopo com base em busca personalizada ou rotina diária
    if marca_alvo:
        foco_varredura = f"foco prioritário e aprofundado no tema/termo '{marca_alvo}' e suas implicações para o iFood"
    else:
        foco_varredura = "foco no ecossistema do iFood, regulação de trabalho por aplicativo (STF, MTE, Congresso), concorrência (Rappi, Zé Delivery, Uber) e reputação corporativa"

    prompt = f"""
Atue como Í.C.A.R.O. (iFood Corporate PR Edition), o motor de inteligência e curadoria editorial corporativa.
Execute a varredura comercial diária e cruzamento de dados de hoje com {foco_varredura}. Foque nas 5 a 10 pautas mais quentes do dia no total.

REGRA DE VERACIDADE ESTRITA: Você SÓ deve incluir pautas se houver fatos factuais e comprovados na mídia nas últimas 48h. Se não houver fatos reais, NÃO INVENTE, NÃO ALUCINE e NÃO INCLUA pautas fictícias.

Identifique oportunidades e riscos nas seguintes frentes estratégicas do iFood:
- Regulação, STF e Legislação (Gig Economy, trabalho por aplicativo, tributação)
- Concorrência e Mercado (Rappi, Zé Delivery, Uber, Mercado Livre, Daki)
- Inovação, Logística e Marketplace
- Gestão de Crise, Reputação Corporativa e ESG

DIRETRIZES PARA A "TÁTICA SUGERIDA" (NÍVEL DIRETOR DE PR):
Atue como um Diretor Sênior de Comunicação Corporativa do iFood. Suas recomendações não podem ser óbvias ou operacionais (NUNCA sugira "fazer press release" ou "postar nas redes").
Sua tática sempre deve começar com um verbo no gerúndio e justificar o impacto no negócio/reputação.
Use EXCLUSIVAMENTE as estratégias e diretrizes do playbook do iFood abaixo:

--- INÍCIO DO PLAYBOOK ---
{playbook_texto}
--- FIM DO PLAYBOOK ---

DIRETRIZES DE SAÍDA (JSON STRICT):
1. Entregue a resposta EXCLUSIVAMENTE em formato de array JSON válido, sem markdown, sem textos antes ou depois.
2. Estrutura de cada objeto: 
   - "tipo": categoria ("regulacao", "concorrencia", "crise" ou "institucional")
   - "titulo": título curto e impactante sobre o fato
   - "agencia": "iFood PR"
   - "setor": frente temática (ex: 'Gig Economy', 'STF/Legislação', 'Marketplace', 'ESG')
   - "marcas": array com entidades envolvidas (ex: ["iFood", "STF"], ["iFood", "Rappi"])
   - "descricao": Fato em 1 frase + Tática sugerida em gerúndio baseada no playbook
   - "produtos": array com 1 a 3 entregáveis de PR (ex: ["Op-Ed", "Posicionamento Institucional", "Mapeamento de Stakeholders"])
   - "link_noticia": URL REAL E EXATA extraída da busca. NUNCA invente ou altere o slug.
   - "data": data de hoje no formato DD/MM/AAAA
   - "imagem": URL de imagem da notícia (se houver) ou string vazia ""
"""

    print("Enviando requisição para a API do Gemini usando o modelo 3.5 Flash...")
    
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            tools=[{"google_search": {}}]
        )
    )
    
    texto_resposta = response.text
    
    if "```json" in texto_resposta:
        texto_resposta = texto_resposta.split("```json")[1].split("```")[0].strip()
    elif "```" in texto_resposta:
        texto_resposta = texto_resposta.split("```")[1].split("```")[0].strip()
        
    texto_resposta = texto_resposta.strip()

    try:
        novas_oportunidades = json.loads(texto_resposta)
        
        # Pós-processamento: Sanitização de links e tratamento duplo de imagens
        print("🔗 Processando e validando URLs e imagens das pautas...")
        for item in novas_oportunidades:
            link_original = item.get("link_noticia", "")
            titulo = item.get("titulo", "")
            imagem_original = item.get("imagem", "")
            categoria = item.get("tipo", "institucional")
            
            # Valida ou gera o link da fonte
            item["link_noticia"] = validar_ou_gerar_link(link_original, titulo)
            
            # Aplica a estratégia em 2 opções para imagem
            item["imagem"] = obter_imagem_valida(imagem_original, categoria)

        historico = []
        if os.path.exists('oportunidades.json'):
            with open('oportunidades.json', 'r', encoding='utf-8') as f:
                conteudo = f.read()
                if conteudo.strip():
                    try:
                        historico = json.loads(conteudo)
                    except json.JSONDecodeError:
                        print("Aviso: O arquivo antigo estava vazio. Iniciando um novo.")
        
        if isinstance(historico, list) and isinstance(novas_oportunidades, list):
            historico.extend(novas_oportunidades)
        else:
            historico = novas_oportunidades
            
        with open('oportunidades.json', 'w', encoding='utf-8') as f:
            json.dump(historico, f, ensure_ascii=False, indent=4)
            
        print("Sucesso! As novas pautas com links e imagens validados foram salvas em 'oportunidades.json'.")
        
    except json.JSONDecodeError:
        print("Erro: A resposta da API não foi um JSON válido. Resposta recebida:")
        print(texto_resposta)
        raise

if __name__ == "__main__":
    gerar_oportunidades()
