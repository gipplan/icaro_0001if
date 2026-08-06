import os
import json
import re
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

    DIRETRIZES DO PLAYBOOK CORPORATIVO:
    {playbook_context}

    INSTRUÇÕES DE PESQUISA (PRIORIDADE MÁXIMA):
    Faça uma busca na web por notícias recentes no Brasil.
    1. É OBRIGATÓRIO incluir resultados recentes para iFood e Stone. Caso a varredura inicial geral não identifique fatos relevantes sobre elas, execute uma busca adicional e direcionada exclusivamente para estas duas marcas. O JSON final DEVE conter pautas para iFood e Stone.
    2. Identifique pautas quentes (5 a 10) abrangendo também os setores: Tecnologia/IA, E-commerce/Logística, ESG/Energia, Finanças/Fintechs, e Aviação/Turismo.
    3. Classifique as pautas nas 6 frentes estratégicas (`regulacao`, `parceiros`, `tecnologia`, `operacao`, `concorrencia`, `esg`, `crise`).

    DIRETRIZES PARA A TÁTICA SUGERIDA (NÍVEL DIRETOR DE PR):
    Atue como um Diretor Sênior de Comunicação Corporativa. Suas recomendações não podem ser óbvias.
    NUNCA sugira "fazer press release", "postar nas redes", "monitorar" ou "fazer Q&A".
    Foco Executivo: PR Stunt, Op-Eds de C-Levels, Ativações em Dark Social, Fóruns Proprietários, Public Affairs/Lobby e Gestão de Crise Avançada.
    Estrutura Obrigatória: A tática (campo recomendacao) sempre deve começar com um verbo no gerúndio e justificar o impacto no negócio da marca.

    FORMATO DE SAÍDA OBRIGATÓRIO (JSON Puro):
    Retorne uma lista JSON válida com as pautas detectadas.
    [
      {{
        "titulo": "Título conciso e direto",
        "resumo_fato": "Resumo executivo, direto e neutro sobre o fato noticiado ou cenário identificado.",
        "recomendacao": "Sua tática recomendada (nível Diretor Sênior), começando sempre com um verbo no gerúndio e justificando o impacto.",
        "tipo": "regulacao" | "parceiros" | "tecnologia" | "operacao" | "concorrencia" | "esg" | "crise",
        "data": "{data_hoje}",
        "setor": "Sub-área específica ou veículo",
        "marcas": ["Marcas envolvidas"],
        "produtos": ["Entregáveis recomendados"],
        "link_noticia": "URL real da notícia",
        "imagem": ""
      }}
    ]

    ATENÇÃO: Responda APENAS com o código JSON válido, sem marcadores ```json ou textos externos.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.2
        )
    )

    texto_resposta = response.text.strip()
    # Limpeza de possíveis marcadores Markdown que o modelo possa inserir por engano
    texto_resposta = re.sub(r'^```json\s*', '', texto_resposta)
    texto_resposta = re.sub(r'^```\s*', '', texto_resposta)
    texto_resposta = re.sub(r'\s*
