# 🤖 SmartShop Cloud — Ecossistema DevOps Inteligente (AIOps)

## 🎯 Objetivo do Projeto

O **SmartShop Cloud** é uma demonstração prática de engenharia de plataforma avançada (**AIOps**), onde pipelines tradicionais de CI/CD foram transformados em sistemas autónomos orientados a contexto. Utilizando o modelo `llama-3.1-8b-instant` via API da Groq, o ecossistema é capaz de inspecionar dados brutos de telemetria, avaliar riscos e tomar decisões operacionais complexas em tempo de execução sem dependência de intervenções humanas manuais.

---

## 🧠 Como a IA pode transformar pipelines tradicionais em sistemas autónomos de DevOps?

Os pipelines de CI/CD tradicionais operam como **esteiras estáticas baseadas em regras determinísticas e rígidas** (ex: se o percentual de cobertura for menor que 80%, a esteira falha). Embora eficientes para tarefas repetitivas, estes sistemas são incapazes de lidar com nuances contextuais, interpretar logs textuais não estruturados de forma holística ou tomar decisões adaptativas baseadas em condições complexas e simultâneas de infraestrutura.

A introdução de Inteligência Artificial Generativa e Large Language Models (LLMs) em ambientes DevOps transforma estas esteiras tradicionais em **sistemas cognitivos autónomos** através de três pilares:

1. **Fusão e Correlação de Contextos Múltiplos:** Ao invés de avaliar métricas e alertas de forma isolada através de regras de código estáticas (_hardcoded_), a IA atua correlacionando dados de naturezas distintas simultaneamente. Ela consegue cruzar um pico quantitativo de hardware (ex: CPU em 92% e latência de 3000ms) com um evento textual específico de erro em logs (ex: _Database Timeout_) e mapear o impacto em cadeia através de um rastro distribuído (ex: _Payment Service_ retendo requisições com código 504). A IA deduz a causa raiz do problema de forma idêntica a um engenheiro de SRE (_Site Reliability Engineering_) sênior.
2. **Tomada de Decisão Cognitiva Adaptativa:** Em cenários de qualidade, falhas parciais em suites de testes causadas por instabilidades efêmeras de infraestrutura (_flaky tests_) costumam travar esteiras inteiras desnecessariamente. Um agente dotado de IA consegue ler a telemetria do ambiente, avaliar semanticamente o impacto real do código produzido na segurança e estabilidade geral e decidir de forma dinâmica se o risco operacional justifica um bloqueio estrutural (`BLOQUEADO`) ou se o fluxo pode avançar com ressalvas (`APROVADO`).
3. **Fechamento Automático do Loop Operacional:** Os pipelines tradicionais limitam-se a notificar falhas de forma passiva (através de e-mails ou alertas em canais de comunicação). Os agentes inteligentes autónomos assumem papel ativo sobre o ciclo de vida do software: eles percebem a degradação, tomam a decisão analítica e **executam ações corretivas e documentais automáticas**, tais como a abertura imediata de chamados técnicos estruturados contendo diagnósticos precisos de causa raiz, isolamento cirúrgico de deploys defeituosos ou geração dinâmica de relatórios executivos de governança.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem Base:** Python 3.11
- **Orquestração de Pipelines:** GitHub Actions (YAML)
- **Framework de Testes e Telemetria:** Pytest & Pytest-Cov
- **Motor de Inteligência Artificial:** Groq Cloud API (`llama-3.1-8b-instant`)

---

## 📂 Estrutura do Repositório

Em conformidade exata com os requisitos arquiteturais exigidos para o projeto, a árvore do repositório está estruturada da seguinte forma:

```text
smartshop-cloud/
├── .github/workflows/
│   ├── quality_gate.yml        # Pipeline do Quality Gate inteligente com IA
│   ├── observability.yml       # Pipeline de Observabilidade e Resposta a Incidentes
│   └── intelligent_agent.yml   # Pipeline do Agente Autónomo de Testes e Docs
├── src/
│   ├── app.py                  # Regra de negócio principal (Carrinho de compras)
│   ├── ai_handlers.py          # Motor de IA (Módulos de Quality Gate e Observabilidade)
│   └── intelligent_agent.py    # Agente Autônomo de Documentação Técnica e QA
├── tests/
│   ├── test_app_good.py        # Suite de testes para cenário de alta cobertura (Sucesso)
│   └── test_app_bad.py         # Suite com asserção incorreta proposital (Simulação de Bloqueio)
├── logs/
│   └── app.log                 # Logs operacionais com registros de anomalias (Database Timeout)
├── metrics/
│   └── metrics.json            # Telemetria com parâmetros críticos de esgotamento de hardware
├── traces/
│   └── trace.txt               # Rastreamento distribuído simulando gargalo em microsserviços
├── security/
│   └── vulnerabilities.json   # Relatório de auditoria de vulnerabilidades gerado dinamicamente
└── docs/
    ├── architecture.md         # Documentação arquitetural de topologia lógica do projeto
    └── relatorio_agente.md     # Relatório analítico gerado de forma 100% autónoma pela IA
```

---

## 🚀 Critérios de Confiabilidade e Observabilidade (SRE)

### O que no projeto SmartShop Cloud seria um sinal de que o deploy não deveria ir para frente?

O deploy será bloqueado imediatamente se a IA ou as ferramentas de telemetria detectarem:

- **Falhas no Checkout (Erros HTTP 5xx > 1%):** Qualquer pico de erro na rota crítica de finalização de pedidos e pagamentos, evitando prejuízos financeiros imediatos.
- **Degradação de Performance (Latência p99 > 800ms):** Aumento excessivo no tempo de resposta da API ou estouro no uso de hardware (**CPU > 80%** ou **Memória > 85%**).
- **Instabilidade no Banco de Dados:** Erros recorrentes de conexão, timeout ou indisponibilidade da camada de persistência (MongoDB/PostgreSQL) registrados nos logs do sistema.
- **Quebra do Quality Gate (Cobertura < 80%):** Envio de código novo ou refatorado sem a cobertura mínima de testes unitários exigida pelos critérios de qualidade do repositório.
