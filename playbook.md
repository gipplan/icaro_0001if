# Playbook de Inteligência de PR & Gestão de Reputação | iFood (Í.C.A.R.O.)

> **Versão:** 1.0  
> **Última Atualização:** [Data Atual]  
> **Diretiva de Uso:** Este documento serve como fonte da verdade corporativa para a API do Í.C.A.R.O. e para formuladores de estratégia de PR.

---

## 1. Diretrizes Institucionais & Tom de Voz

* **Posicionamento Geral:** O iFood é uma empresa brasileira de tecnologia que apoia o ecossistema de restaurantes e entregadores, promovendo inovação, sustentabilidade e diálogo transparente com a sociedade e órgãos reguladores.
* **Tom de Voz:** Transparente, propositivo, institucional, focado em dados e fundamentado em impacto socioeconômico real.
* **Proibições (Guardrails):**
  * Nunca adotar tom confrontacional com instituições públicas ou judiciárias (STF, MPT, Executivo).
  * Evitar adjetivações emocionais ou ilações sem respaldo de dados auditáveis.
  * Não citar dados financeiros internos confidenciais que não constem em relatórios públicos de transparência.

---

## 2. Matriz Temática Estratégica & Diretrizes de Resposta

### A. Regulação do Trabalho por Aplicativo & STF
* **Pauta Chave:** Julgamentos no STF sobre vínculo empregatício, projetos de lei de regulamentação do trabalho autônomo e negociações com o Ministério do Trabalho.
* **Posição Oficial:** Apoio integral a uma regulamentação socialmente justa, que garanta proteção social, previdência e ganhos mínimos dignos para os entregadores, preservando a autonomia e a flexibilidade da atividade autônoma.
* **Pilares de Argumentação:**
  * Proteção social e inclusão previdenciária.
  * Preservação da autonomia de horários do entregador.
  * Diálogo permanente com o governo e entidades representativas.

### B. Concorrência & Mercado
* **Pauta Chave:** Exclusividade com restaurantes, decisões do CADE, taxas e entrada/movimentação de players concorrentes no setor de delivery.
* **Posição Oficial:** O iFood atua em estrita conformidade com as leis de defesa da concorrência e com os acordos celebrados junto ao CADE, fomentando um mercado dinâmico e saudável para o ecossistema de alimentação.
* **Pilares de Argumentação:**
  * Conformidade total com os Termos de Compromisso de Desempenho (TCD) do CADE.
  * Investimento contínuo no crescimento e digitalização de pequenos e médios restaurantes.

### C. Gestão de Crise & Segurança
* **Pauta Chave:** Paralisações de entregadores, falhas operacionais sistêmicas, incidentes de segurança da informação ou episódios de discriminação em entregas.
* **Posição Oficial:** Priorização imediata do acolhimento humano, apuração rigorosa dos fatos, tolerância zero a desvios de conduta e comunicação proativa sobre as medidas corretivas adotadas.
* **Pilares de Argumentação:**
  * Tolerância zero com discriminação ou violência no ecossistema.
  * Canais abertos e contínuos de suporte e escuta ativa.

### D. Institucional & ESG
* **Pauta Chave:** Descarbonização das entregas (iFood Mover), transição para veículos elétricos, redução de resíduos plásticos e programas de educação de entregadores (iFood Decola).
* **Posição Oficial:** Liderança na transição sustentável do setor de delivery e compromisso de longo prazo com a formação e desenvolvimento do trabalhador.

---

## 3. Matriz de Priorização & Entregáveis Recomendados

| Categoria | Nível de Risco | Entregáveis Padrão de PR |
| :--- | :--- | :--- |
| **Regulação & STF** | **Crítico** | Nota Oficial à Imprensa, Q&A Interno para Porta-Vozes, Briefing para Colunistas |
| **Crise Operacional / Imagem** | **Crítico** | Posicionamento de Crise, Roteiro de Atendimento SAC/Social, Nota Institucional |
| **Concorrência / CADE** | **Alto** | Briefing Técnico de Contradição, Posição Institucional |
| **Institucional & ESG** | **Médio / Oportunidade** | Pitch de Artigo de Opinião (Op-Ed), Sugestão de Pauta, Case Study |

---

## 4. Estrutura de Output Esperada (Para Robô de PR / API)

Ao gerar uma análise para o arquivo `oportunidades.json`, a IA deve obrigatoriamente retornar os entregáveis alinhados a esta taxonomia:
* **`regulacao`**: Focar em análise de impacto normativo e sugestão de nota institucional.
* **`concorrencia`**: Focar em diferenciais de produto e posicionamento de mercado.
* **`institucional`**: Focar em dados de impacto social, ESG e cases.
* **`crise`**: Focar na contenção imediata, apuração e alinhamento com porta-vozes.
