import os
import json
from datetime import datetime
from google import genai
from google.genai import types

def carregar_playbook():
    path = "playbook.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Playbook padrão não encontrado."

def carregar_oportunidades_existentes():
    path = "oportunidades.json"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def executar_varredura():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não encontrada.")

    client = genai.Client(api_key=api_key)
    playbook_context = carregar_playbook()
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    prompt = f"""
    Você é o robô Í.C.A.R.O., a central autônoma de inteligência de PR e reputação do iFood.
    Data da varredura: {data_hoje}

    DIRETRIZES DO PLAYBOOK CORPORATIVO (SEU NORTE ESTRATÉGICO):
    {playbook_context}

    INSTRUÇÕES DE PESQUISA (PRIORIDADE MÁXIMA):
    Faça uma busca na web por notícias recentes no Brasil.
    1. É OBRIGATÓRIO incluir resultados recentes para iFood e Stone. Caso a varredura inicial geral não identifique fatos relevantes sobre elas, execute uma busca adicional e direcionada exclusivamente para estas duas marcas. O JSON final DEVE conter pautas para iFood e Stone.
    2. Identifique pautas quentes (5 a 10) abrangendo também os setores: Tecnologia/IA, E-commerce/Logística, ESG/Energia, Finanças/Fintechs, e Aviação/Turismo.
    3. Classifique as pautas nas 6 frentes estratégicas (`regulacao`, `parceiros`, `tecnologia`, `operacao`, `concorrencia`, `esg`, `crise`).

    DIRETRIZES PARA A TÁTICA SUGERIDA (MINDSET: DIRETOR DE PR CRIATIVO E OUSADO):
    Atue como um Diretor Sênior de Comunicação altamente criativo e focado em negócios. 
    O Playbook corporativo acima serve APENAS como base para você saber o que importa para a empresa (nossos produtos, visão de IA, metas de ESG). 
    
    REGRAS DE CRIATIVIDADE OBRIGATÓRIAS:
    - NÃO seja burocrático. Nunca cite na tática fluxos internos, aprovações, e-mails ou canais de Slack.
    - Fuja do óbvio. NUNCA sugira "fazer press release", "postar nas redes", "monitorar" ou "fazer Q&A".
    - Pense grande: Newsjacking, Vazamentos Controlados (Dark Social), Coalizões Incomuns, PR Stunts de guerrilha, Thought Leadership provocativo e Advocacy invisível.
    - Estrutura: Comece SEMPRE com um verbo no gerúndio. A tática deve conectar a notícia quente a um dos pilares do playbook, mostrando como a ação hackeia a narrativa pública para gerar valor de negócio (reputação ou blindagem).

    FORMATO DE SAÍDA OBRIGATÓRIO (JSON Puro):
    Retorne uma lista JSON válida com as pautas detectadas.
    [
      {{
        "titulo": "Título conciso e direto",
        "resumo_fato": "Resumo executivo, direto e neutro sobre o fato noticiado.",
        "recomendacao": "Sua tática criativa (nível Diretor Sênior), começando sempre com um verbo no gerúndio e focada em PR de impacto.",
        "tipo": "regulacao" | "parceiros" | "tecnologia" | "operacao" | "concorrencia" | "esg" | "crise",
        "data": "{data_hoje}",
        "setor": "Sub-área específica ou veículo",
        "marcas": ["Marcas envolvidas"],
        "produtos": ["Entregáveis recomendados"],
        "link_noticia": "URL real da notícia",
        "imagem": ""
      }}
    ]

    ATENÇÃO: Responda APENAS com o código JSON válido.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.3 # Leve aumento na temperatura para permitir táticas mais criativas
        )
    )

    texto_resposta = response.text.strip()
    
    # Limpeza segura da formatação markdown
    if texto_resposta.startswith("```json"):
        texto_resposta = texto_resposta[7:]
    elif texto_resposta.startswith("```"):
        texto_resposta = texto_resposta[3:]

    if texto_resposta.endswith("```"):
        texto_resposta = texto_resposta[:-3]

    texto_resposta = texto_resposta.strip()

    try:
        novas_pautas = json.loads(texto_resposta)
    except json.JSONDecodeError as e:
        print("Erro ao decodificar JSON retornado pelo Gemini:", e)
        print("Conteúdo recebido:")
        print(texto_resposta)
        return

    pautas_existentes = carregar_oportunidades_existentes()
    titulos_existentes = {p.get("titulo", "").strip().lower() for p in pautas_existentes}
    
    pautas_adicionadas = 0
    for pauta in novas_pautas:
        titulo_limpo = pauta.get("titulo", "").strip().lower()
        if titulo_limpo not in titulos_existentes:
            pautas_existentes.insert(0, pauta)
            titulos_existentes.add(titulo_limpo)
            pautas_adicionadas += 1

    pautas_finais = pautas_existentes[:50]

    with open("oportunidades.json", "w", encoding="utf-8") as f:
        json.dump(pautas_finais, f, ensure_ascii=False, indent=2)

    print(f"Sucesso! Varredura web concluída. {pautas_adicionadas} novas pautas adicionadas.")

if __name__ == "__main__":
    executar_varredura()
