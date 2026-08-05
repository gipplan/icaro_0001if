import os
import json
import re
from datetime import datetime
from google import genai
from google.genai import types

def carregar_playbook():
    """Lê o arquivo de conhecimento do iFood."""
    caminho_playbook = 'playbook.md'
    if os.path.exists(caminho_playbook):
        with open(caminho_playbook, 'r', encoding='utf-8') as f:
            return f.read()
    print(f"⚠️ Aviso: Arquivo {caminho_playbook} não encontrado. Operando com prompt padrão.")
    return ""

def limpar_resposta_json(texto_resposta):
    """Remove marcações de markdown ```json do retorno do modelo."""
    texto_limpo = re.sub(r'```json\s*', '', texto_resposta)
    texto_limpo = re.sub(r'```\s*$', '', texto_limpo)
    return texto_limpo.strip()

def rodar_motor_icaro():
    # 1. Leitura de variáveis de ambiente e arquivos
    api_key = os.environ.get("GEMINI_API_KEY")
    marca_alvo = os.environ.get("MARCA_ALVO", "").strip()
    
    if not api_key:
        raise ValueError("❌ Erro: GEMINI_API_KEY não configurada nas variáveis de ambiente.")

    playbook_conteudo = carregar_playbook()
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    # 2. Definição do escopo de busca
    if marca_alvo:
        termo_varredura = f"foco prioritário na marca/entidade '{marca_alvo}' e suas implicações para o ecossistema do iFood"
    else:
        termo_varredura = "varredura geral do ecossistema iFood, regulação de aplicativos (STF/Governo), concorrência (Rappi, Zé Delivery, Uber) e pautas trabalhistas/gig economy"

    # 3. Construção do Prompt Estratégico
    prompt = f"""
Você é o motor de inteligência estratégica do sistema I.C.A.R.O. (iFood Corporate PR Edition).
Data atual de referência: {data_hoje}.

DIRETRIZES DO PLAYBOOK IFOOD:
{playbook_conteudo}

SUA MISSÃO:
Realize uma busca web em tempo real sobre: {termo_varredura}.
Identifique de 3 a 5 fatos recentes e relevantes (últimas 24-48 horas) e estruture táticas de Relações Públicas.

REGRAS OBRIGATÓRIAS DE SAÍDA:
- O retorno DEVE ser EXCLUSIVAMENTE um array JSON válido (sem textos introdutórios ou conclusivos).
- Cada objeto do array deve seguir rigorosamente a estrutura de chaves abaixo:

[
  {{
    "titulo": "Título curto e de alto impacto sobre o fato",
    "tipo": "Uma das categorias: 'regulacao', 'concorrencia', 'crise' ou 'institucional'",
    "setor": "Frente temática (ex: 'Gig Economy', 'STF/Legislação', 'Marketplace', 'Logística')",
    "data": "{data_hoje}",
    "marcas": ["Lista de entidades envolvidas, ex: iFood, STF, Rappi, Ministério do Trabalho"],
    "descricao": "O Fato em 1 frase objetiva. Tática Sugerida (PR) em gerúndio destacando a recomendação estratégica.",
    "produtos": ["Táticas de PR envolvidas, ex: 'Op-Ed', 'PR Stunt', 'Gerenciamento de Crise', 'Notas Oficiais']",
    "link_noticia": "URL real da fonte primária encontrada na busca ou link para busca Google News referente ao fato",
    "imagem": ""
  }}
]
"""

    print("🚀 Inicializando cliente Google GenAI...")
    client = genai.Client(api_key=api_key)

    print("🔍 Realizando varredura web com Google Search Grounding...")
  response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            tools=[{"google_search": {}}]
        )
    )

    # 4. Tratamento e Validação da Resposta
    conteudo_resposta = limpar_resposta_json(response.text)
    
    try:
        novas_oportunidades = json.loads(conteudo_resposta)
        if not isinstance(novas_oportunidades, list):
            raise ValueError("O retorno do modelo não é uma lista JSON válida.")
    except Exception as e:
        print(f"❌ Erro ao parsear JSON retornado pelo Gemini: {e}")
        print("Resposta bruta recebida:\n", response.text)
        return

    # 5. Atualização do Banco de Dados Local (oportunidades.json)
    arquivo_json = "oportunidades.json"
    dados_existentes = []

    if os.path.exists(arquivo_json):
        try:
            with open(arquivo_json, 'r', encoding='utf-8') as f:
                dados_existentes = json.load(f)
        except Exception:
            dados_existentes = []

    # Mescla novas oportunidades garantindo a desduplicação simples por título
    titulos_existentes = {item.get("titulo", "").strip().lower() for item in dados_existentes}
    itens_adicionados = 0

    for item in novas_oportunidades:
        titulo = item.get("titulo", "").strip().lower()
        if titulo and titulo not in titulos_existentes:
            dados_existentes.insert(0, item) # Insere no topo
            titulos_existentes.add(titulo)
            itens_adicionados += 1

    # Salva o arquivo atualizado
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(dados_existentes, f, ensure_ascii=False, indent=4)

    print(f"✅ Sucesso! {itens_adicionados} novas pautas adicionadas ao 'oportunidades.json'. Total na base: {len(dados_existentes)}")

if __name__ == "__main__":
    rodar_motor_icaro()
