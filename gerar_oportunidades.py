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

    INSTRUÇÕES DE PESQUISA:
    Faça uma busca na web por notícias recentes relacionadas ao ecossistema do iFood e ao setor de delivery/tecnologia.
    Varra as 6 frentes estratégicas:
    1. Regulação do Trabalho, STF, MPT (`regulacao`)
    2. Relação com Restaurantes, PMEs, Comissões (`parceiros`)
    3. Algoritmos, Bloqueios, Golpe da Maquininha, IA (`tecnologia`)
    4. Paralisações, Pontos de Apoio (`operacao`)
    5. CADE, Concorrência, Supermercados (`concorrencia`)
    6. Frota Elétrica, Redução de Plástico (`esg`)
    7. Gestão de Crise (`crise`)

    FORMATO DE SAÍDA OBRIGATÓRIO (JSON Puro):
    Retorne uma lista JSON com até 8 pautas detectadas.
    [
      {{
        "titulo": "Título conciso e direto",
        "descricao": "Resumo do fato e análise do impacto reputacional/estratégico.",
        "tipo": "regulacao" | "parceiros" | "tecnologia" | "operacao" | "concorrencia" | "esg" | "crise",
        "data": "{data_hoje}",
        "setor": "Sub-área específica",
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
    texto_resposta = re.sub(r'^```json\s*', '', texto_resposta)
    texto_resposta = re.sub(r'^```\s*', '', texto_resposta)
    texto_resposta = re.sub(r'\s*```$', '', texto_resposta)

    novas_pautas = json.loads(texto_resposta)
    pautas_existentes = carregar_oportunidades_existentes()

    # Preserva o histórico e adiciona apenas o que for inédito
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

    print(f"Sucesso! Varredura concluída. {pautas_adicionadas} novas pautas web adicionadas ao portal.")

if __name__ == "__main__":
    executar_varredura()
