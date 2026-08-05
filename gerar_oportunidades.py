import os
import json
import re
from google import genai
from google.genai import types

def carregar_playbook():
    try:
        with open('playbook.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Nenhum playbook personalizado encontrado. Siga as diretrizes de Diretor Sênior de PR do iFood."

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
   - "link_noticia": URL real da notícia ou link de busca direta do fato
   - "data": data de hoje no formato DD/MM/AAAA
   - "imagem": URL de imagem da notícia/banco de imagens ou string vazia ""
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
        # 1. Transforma o resultado de hoje em uma lista Python
        novas_oportunidades = json.loads(texto_resposta)
        
        # 2. Prepara uma lista vazia para o histórico
        historico = []
        
        # 3. Se o arquivo já existir, lê o que tem lá dentro e guarda na lista de histórico
        if os.path.exists('oportunidades.json'):
            with open('oportunidades.json', 'r', encoding='utf-8') as f:
                conteudo = f.read()
                if conteudo.strip():
                    try:
                        historico = json.loads(conteudo)
                    except json.JSONDecodeError:
                        print("Aviso: O arquivo antigo estava vazio ou inválido. Iniciando um novo.")
        
        # 4. Junta as duas listas (a velha e a nova)
        if isinstance(historico, list) and isinstance(novas_oportunidades, list):
            historico.extend(novas_oportunidades)
        else:
            historico = novas_oportunidades
            
        # 5. Salva a lista gigante e atualizada de volta no arquivo json, usando formatação bonita
        with open('oportunidades.json', 'w', encoding='utf-8') as f:
            json.dump(historico, f, ensure_ascii=False, indent=4)
            
        print("Sucesso! As novas pautas do iFood foram adicionadas ao histórico do oportunidades.json.")
        
    except json.JSONDecodeError:
        print("Erro: A resposta da API não foi um JSON válido. Veja a resposta crua:")
        print(texto_resposta)
        raise

if __name__ == "__main__":
    gerar_oportunidades()
