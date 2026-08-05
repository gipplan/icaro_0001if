import os
import sys
import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from google import genai
from google.genai import types

def extrair_texto_boxnet(url):
    """Baixa a página da Boxnet e extrai o texto limpo do clipping."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()
        
    texto_limpo = soup.get_text(separator='\n')
    linhas = [line.strip() for line in texto_limpo.splitlines() if line.strip()]
    return "\n".join(linhas)

def carregar_playbook():
    path = "playbook.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Playbook padrão."

def carregar_oportunidades_existentes():
    path = "oportunidades.json"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def analisar_clipping(url_clipping):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada.")

    client = genai.Client(api_key=api_key)
    playbook_context = carregar_playbook()
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    print(f"Baixando conteúdo do clipping: {url_clipping}")
    conteudo_clipping = extrair_texto_boxnet(url_clipping)
    print(f"Conteúdo extraído ({len(conteudo_clipping)} caracteres). Enviando para análise do Gemini...")

    prompt = f"""
    Você é o robô Í.C.A.R.O., central autônoma de PR e inteligência de reputação do iFood.
    Data da análise: {data_hoje}

    DIRETRIZES DO PLAYBOOK CORPORATIVO:
    {playbook_context}

    CONTEÚDO BRUTO DO CLIPPING DIÁRIO (BOXNET):
    {conteudo_clipping[:150000]}

    TAREFA:
    Análise as notícias deste clipping da Boxnet. Identifique as pautas relevantes que impactam direta ou indiretamente o iFood, seus concorrentes, entregadores, restaurantes ou o mercado de foodtech/delivery.

    Classifique cada pauta em uma das 6 frentes estratégicas do playbook:
    - `regulacao`: Leis, STF, MPT, Trabalho Autônomo.
    - `parceiros`: Restaurantes, PMEs, Comissões, Repasses.
    - `tecnologia`: Algoritmos, Bloqueios, Golpe da Maquininha, Segurança, IA.
    - `operacao`: Paralisações, Pontos de Apoio, Condições de Trabalho.
    - `concorrencia`: CADE, Concorrentes, Mercado, Supermercados (Grocery).
    - `esg`: Veículos Elétricos, Embalagens, Ações Sociais.
    - `crise`: Imagem, Riscos Graves e Urgências.

    FORMATO DE SAÍDA OBRIGATÓRIO (JSON Puro):
    Retorne uma lista JSON com as pautas encontradas.
    [
      {{
        "titulo": "Manchete/Título da notícia no clipping",
        "descricao": "Resumo executivo do fato e recomendação estratégica de PR alinhada ao playbook.",
        "tipo": "regulacao" | "parceiros" | "tecnologia" | "operacao" | "concorrencia" | "esg" | "crise",
        "data": "{data_hoje}",
        "setor": "Veículo de imprensa ou editoria",
        "marcas": ["Marcas envolvidas"],
        "produtos": ["Entregáveis recomendados de PR"],
        "link_noticia": "{url_clipping}",
        "imagem": ""
      }}
    ]

    ATENÇÃO: Responda APENAS com o código JSON válido, sem marcadores ```json ou explicações.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1)
    )

    texto_resposta = response.text.strip()
    texto_resposta = re.sub(r'^```json\s*', '', texto_resposta)
    texto_resposta = re.sub(r'^```\s*', '', texto_resposta)
    texto_resposta = re.sub(r'\s*```$', '', texto_resposta)

    novas_pautas = json.loads(texto_resposta)
    pautas_existentes = carregar_oportunidades_existentes()

    # Lógica de Merge: Adiciona novas pautas evitando duplicatas por título
    titulos_existentes = {p.get("titulo", "").strip().lower() for p in pautas_existentes}
    
    pautas_adicionadas = 0
    for pauta in novas_pautas:
        titulo_limpo = pauta.get("titulo", "").strip().lower()
        if titulo_limpo not in titulos_existentes:
            pautas_existentes.insert(0, pauta) # Adiciona no topo
            titulos_existentes.add(titulo_limpo)
            pautas_adicionadas += 1

    # Mantém um teto máximo de 50 pautas para manter o JSON leve
    pautas_finais = pautas_existentes[:50]

    with open("oportunidades.json", "w", encoding="utf-8") as f:
        json.dump(pautas_finais, f, ensure_ascii=False, indent=2)

    print(f"Sucesso! {pautas_adicionadas} novas pautas do clipping foram incorporadas ao portal (Total acumulado: {len(pautas_finais)}).")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url_input = sys.argv[1]
    else:
        url_input = input("Cole a URL do clipping da Boxnet: ")
    
    analisar_clipping(url_input)
