1. playbook.md (Atualizado com as 6 Frentes Estratégicas)
Markdown
# Playbook de Inteligência de PR & Gestão de Reputação | iFood (Í.C.A.R.O.)

> **Versão:** 2.0 (Expandida)  
> **Diretiva de Uso:** Fonte da verdade corporativa para o motor de IA e para a tomada de decisão da equipe de Comunicação Corporativa e Public Affairs.

---

## 1. Diretrizes Institucionais & Guardrails

* **Posicionamento Institucional:** O iFood é uma empresa brasileira de tecnologia que fomenta o ecossistema de alimentação e entregas, aliando inovação, desenvolvimento socioeconômico e diálogo contínuo com a sociedade e instâncias governamentais.
* **Tom de Voz:** Propositivo, transparente, fundamentado em dados auditáveis, focado na construção de pontes e com alto rigor técnico.
* **Guardrails (Proibições de PR):**
  * Não adotar tom confrontacional com instituições públicas, tribunais superiores (STF/TST), órgãos reguladores ou sindicatos.
  * Não especular sobre decisões judiciais em andamento sem parecer técnico da equipe jurídica.
  * Evitar adjetivações emocionais ou acusações diretas contra concorrentes.
  * Nunca divulgar dados financeiros confidenciais ou métricas operacionais não auditadas publicamente.

---

## 2. Matriz das 6 Frentes Estratégicas de Observação

### A. Regulação do Trabalho por Aplicativo & STF (`regulacao`)
* **Foco:** Julgamentos no STF, projetos de lei de regulamentação do trabalho autônomo, negociações no Ministério do Trabalho e acordos coletivos.
* **Posição Oficial:** Apoio à criação de um marco regulatório nacional que garanta proteção social, previdência e ganhos dignos, mantendo a autonomia e flexibilidade de horários do entregador.
* **Entregáveis:** Nota Oficial Institucional, Q&A para Porta-Vozes, Briefing de Background para Colunistas.

### B. Ecossistema de Restaurantes & PMEs (`parceiros`)
* **Foco:** Alterações em taxas de comissão, prazos de repasse financeiro, contratos de exclusividade, migração para canais próprios (WhatsApp/Delivry) e apoio a pequenos e médios estabelecimentos.
* **Posição Oficial:** O iFood é um parceiro impulsionador do setor de alimentação fora do lar, oferecendo tecnologia, inteligência de dados e visibilidade para que pequenos negócios cresçam com rentabilidade.
* **Entregáveis:** Comunicado a Parceiros, Relatório de Impacto Econômico, Case Study de PME.

### C. Governança Algorítmica, Tecnologia & Fraudes (`tecnologia`)
* **Foco:** Transparência de algoritmos (alocação de pedidos e rotas), bloqueios de contas, "golpe da maquininha", segurança da informação, LGPD e Inteligência Artificial.
* **Posição Oficial:** Compromisso com a governança algorítmica ética, tolerância zero a fraudes e investimento constante em biometria e camadas de proteção para consumidores, entregadores e restaurantes.
* **Entregáveis:** Nota Explicativa Técnica, Guia de Prevenção a Golpes, Artigo de Opinião sobre Tecnologia Ética.

### D. Operação Local, Diálogo Sindical & Segurança (`operacao`)
* **Foco:** Paralisações regionais de entregadores ("breques"), pontos de apoio (Espaços iFood), condições de trabalho sob eventos climáticos extremos e seguros de saúde/acidente.
* **Posição Oficial:** Diálogo aberto e contínuo com lideranças locais e sindicatos, priorizando a segurança física e o bem-estar operacional dos entregadores parceiros.
* **Entregáveis:** Posicionamento Local de Praça, Balanço de Cobertura de Seguros, Informativo de Infraestrutura.

### E. Concorrência, Mercado & Quick-Commerce (`concorrencia`)
* **Foco:** Termos de Compromisso do CADE, movimentações de concorrentes no setor de delivery, expansão no segmento de supermercados (iFood Mercado) e inovação logística (drones/robôs).
* **Posição Oficial:** Atuação em estrita conformidade com as regras de livre concorrência e com as determinações do CADE, promovendo um mercado diverso e dinâmico.
* **Entregáveis:** Briefing Técnico de Mercado, Posicionamento Mercadológico, Press Release de Inovação.

### F. Sustentabilidade, Impacto Social & ESG (`esg`)
* **Foco:** Transição para frota elétrica (iFood Mover), meta de descarbonização, redução do uso de plásticos e iniciativas de formação e escolaridade (iFood Decola).
* **Posição Oficial:** Liderança da agenda ESG na logística da América Latina, investindo na descarbonização da cadeia e no desenvolvimento educacional do ecossistema.
* **Entregáveis:** Pitch para Editorias de ESG, Balanço de Impacto Ambiental, Sugestão de Pauta Social.

---

## 3. Matriz Taxonômica de Categorias no Sistema

| Código da Categoria | Nome Amigável (Interface) | Ícone da Interface |
| :--- | :--- | :--- |
| `regulacao` | Regulação & STF | `fa-gavel` |
| `parceiros` | Restaurantes & PMEs | `fa-store` |
| `tecnologia` | Algoritmos & Fraudes | `fa-microchip` |
| `operacao` | Trabalhista & Operação | `fa-person-biking` |
| `concorrencia` | Concorrência & Mercado | `fa-chart-line` |
| `esg` | ESG & Sustentabilidade | `fa-leaf` |
| `crise` | Gestão de Crise | `fa-shield-halved` |
2. gerar_oportunidades.py (Script de Varredura Automatizada)
Python
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

def executar_varredura():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A variável de ambiente GEMINI_API_KEY não foi encontrada.")

    client = genai.Client(api_key=api_key)
    playbook_context = carregar_playbook()
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    prompt = f"""
    Você é o robô Í.C.A.R.O., a central autônoma de inteligência de PR e reputação do iFood.
    Data da varredura: {data_hoje}

    DIRETRIZES DO PLAYBOOK CORPORATIVO:
    {playbook_context}

    INSTRUÇÕES DE PESQUISA:
    Faça uma busca na web por notícias e acontecimentos recentes no Brasil relacionados ao ecossistema do iFood e ao setor de delivery/tecnologia.
    Varra obrigatoriamente as 6 frentes estratégicas de observação:
    1. Regulação do Trabalho, STF, MPT e Leis (`regulacao`)
    2. Relação com Restaurantes, PMEs, Comissões e Repasses (`parceiros`)
    3. Governança Algorítmica, Bloqueios, Golpe da Maquininha e IA (`tecnologia`)
    4. Paralisações de Entregadores, Pontos de Apoio e Clima (`operacao`)
    5. CADE, Concorrência, Supermercados e Mercado (`concorrencia`)
    6. Frota Elétrica, Redução de Plástico e Projetos Sociais (`esg`)
    7. Casos de Urgência Imagem / Crise Grave (`crise`)

    FORMATO DE SAÍDA OBRIGATÓRIO (JSON Puro):
    Retorne uma lista JSON com até 8 oportunidades detectadas.
    Cada item do array deve obrigatoriamente conter a seguinte estrutura:
    [
      {{
        "titulo": "Título conciso e direto sobre a pauta",
        "descricao": "Resumo do fato e análise do impacto reputacional/estratégico para o iFood.",
        "tipo": "regulacao" | "parceiros" | "tecnologia" | "operacao" | "concorrencia" | "esg" | "crise",
        "data": "{data_hoje}",
        "setor": "Sub-área específica (ex: STF, Fraudes, PMEs, CADE, ESG)",
        "marcas": ["iFood", "MarcaConcorrenteOuParceiro"],
        "produtos": ["Nome do Entregável de PR Sugerido 1", "Nome do Entregável 2"],
        "link_noticia": "URL real e direta da notícia encontrada",
        "imagem": "URL válida da imagem da notícia ou string vazia ''"
      }}
    ]

    ATENÇÃO: Responda APENAS com o código JSON válido, sem marcadores ```json ou explicações externas.
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
    
    # Limpeza do JSON
    texto_resposta = re.sub(r'^```json\s*', '', texto_resposta)
    texto_resposta = re.sub(r'^```\s*', '', texto_resposta)
    texto_resposta = re.sub(r'\s*```$', '', texto_resposta)

    try:
        oportunidades = json.loads(texto_resposta)
    except json.JSONDecodeError as e:
        print("Erro ao decodificar JSON gerado pelo Gemini. Conteúdo bruto:")
        print(texto_resposta)
        raise e

    # Persistência no oportunidades.json
    with open("oportunidades.json", "w", encoding="utf-8") as f:
        json.dump(oportunidades, f, ensure_ascii=False, indent=2)

    print(f"Sucesso! {len(oportunidades)} pautas capturadas e salvas em oportunidades.json")

if __name__ == "__main__":
    executar_varredura()
