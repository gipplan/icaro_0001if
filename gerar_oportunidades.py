import os
import json
from google import genai
from google.genai import types

def carregar_notebook():
    """
    Carrega as diretrizes institucionais do iFood.
    Mantenha o arquivo playbook.md no repositório para funcionar como o 'Gemini Notebook'.
    """
    try:
        with open('playbook.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Nenhuma diretriz institucional encontrada. Siga o bom senso de um Diretor Sênior de PR."

def gerar_oportunidades():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave da API não encontrada nas variáveis de ambiente.")
    
    client = genai.Client(api_key=api_key)
    
    print("🔍 Diagnosticando modelos e iniciando o I.C.A.R.O. - iFood Edition...")
    
    notebook_texto = carregar_notebook()

    prompt = f"""
Você é o "I.C.A.R.O. Engine - Edição iFood", operando no MODO 1: INTELIGÊNCIA DIÁRIA AUTOMATIZADA (RADAR DE PR).
Assuma imediatamente sua persona de Diretor Sênior de PR do iFood.

⚠️ PRIORIDADE MÁXIMA (FORÇAR BUSCA): É obrigatório pesquisar na web agora as notícias reais das últimas 24/48 horas sobre o iFood, aplicativos de entrega (ex: Rappi, Zé Delivery), gig economy, regulação de trabalho (STF, Ministério do Trabalho) e concorrência.
**REGRA DE VERACIDADE:** NÃO INVENTE, NÃO ALUCINE. Só inclua pautas baseadas em fatos reais e noticiosos publicados na mídia.

**Diretrizes Estratégicas:**
1. Cruze obrigatoriamente as informações reais encontradas na web com a base de conhecimento institucional abaixo (sua fonte de verdade corporativa):
--- INÍCIO DA BASE DE CONHECIMENTO ---
{notebook_texto}
--- FIM DA BASE DE CONHECIMENTO ---

2. Proponha abordagens não-convencionais e inovadoras de PR. 
3. Você está TERMINANTEMENTE PROIBIDO de sugerir ações triviais (ex: "fazer press release", "postar nas redes sociais"). 
4. Foque exclusivamente em: PR Stunt, Op-Eds (Artigos de Opinião), Dark Social, Public Affairs, Fóruns Proprietários e Gestão de Crise.
5. A `"descricao"` deve OBRIGATORIAMENTE iniciar com um verbo no gerúndio (ex: Articulando, Estruturando, Liderando, Neutralizando) e justificar o impacto no negócio.

**Diretrizes de Saída (JSON STRICT):**
Sua resposta deve ser EXCLUSIVAMENTE um array de objetos JSON válido e minificado contendo as 5 principais pautas/táticas do dia. 
Não inclua saudações, resumos, crases ou marcação markdown (```json) fora do array.

Esquema EXATO do JSON para cada objeto da lista:
- "tipo": (ex: "regulacao", "concorrencia", "crise", "institucional")
- "titulo": (O tema macro da notícia)
- "agencia": "iFood In-house"
- "setor": "Foodtech & Gig Economy"
- "marcas": (Array com as marcas/órgãos envolvidos no fato)
- "descricao": (A tática sugerida começando com verbo no gerúndio)
- "produtos": (Array com até 3 frentes de PR sugeridas)
- "link_noticia": (URL real da matéria encontrada na busca)
- "data": (Data de hoje no formato DD/MM/AAAA)
- "imagem": (URL de uma imagem ilustrativa genérica relacionada ao tema, busque fotos de bancos de imagens gratuitos)
"""

    print("Enviando requisição para a API do Gemini com Google Search Grounding...")
    
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            tools=[{"google_search": {}}]
        )
    )
    
    texto_resposta = response.text
    
    # Tratamento da formatação Markdown se o modelo insistir em enviar
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
        
        # 3. Lê o banco de dados atual se ele existir
        if os.path.exists('oportunidades.json'):
            with open('oportunidades.json', 'r', encoding='utf-8') as f:
                conteudo = f.read()
                if conteudo.strip():
                    try:
                        historico = json.loads(conteudo)
                    except json.JSONDecodeError:
                        print("Aviso: O arquivo antigo estava vazio ou inválido. Iniciando um novo.")
        
        # 4. Junta os arrays
        if isinstance(historico, list) and isinstance(novas_oportunidades, list):
            historico.extend(novas_oportunidades)
        else:
            historico = novas_oportunidades
            
        # 5. Salva de volta no banco de dados
        with open('oportunidades.json', 'w', encoding='utf-8') as f:
            json.dump(historico, f, ensure_ascii=False, indent=4)
            
        print("🚀 Sucesso! O radar executivo do iFood foi atualizado no arquivo oportunidades.json.")
        
    except json.JSONDecodeError:
        print("❌ Erro: A resposta da API não foi um JSON válido. Veja o output cru para depurar:")
        print(texto_resposta)
        raise

if __name__ == "__main__":
    gerar_oportunidades()
