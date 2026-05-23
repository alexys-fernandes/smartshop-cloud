# Documentação de Arquitetura - SmartShop Cloud 🤖

## Objetivo do Projeto

O SmartShop Cloud é um sistema de carrinho de compras automatizado e integrado com IA Generativa (Groq API + Llama 3.1) para aplicar conceitos avançados de IA em operações DevOps (AIOps).

## Estrutura do Repositório

Conforme os requisitos da atividade, o projeto segue a seguinte árvore de diretórios:

- `.github/workflows/`: Pipelines de CI/CD (Quality Gate, Observabilidade e Agente de Testes).
- `src/`: Código fonte (`app.py`, `ai_handlers.py`, `intelligent_agent.py`).
- `tests/`: Bateria de testes unitários (`test_app_good.py`, `test_app_bad.py`).
- `logs/`: Logs de auditoria operacional do sistema (`app.log`).
- `metrics/`: Métricas de hardware e latência em tempo real (`metrics.json`).
- `traces/`: Rastreamento distribuído de requisições (`trace.txt`).
- `security/`: Relatórios de auditoria e varredura de segurança do ecossistema (`vulnerabilities.json`).
- `docs/`: Arquivos de documentação técnica e de arquitetura (`architecture.md`).

## Componentes Inteligentes

1. **Quality Gate:** Bloqueia automaticamente merges se a cobertura de testes do pytest cair abaixo de 80% ou contiver erros lógicos.
2. **Agente de Observabilidade:** Avalia os logs estressados, consumo de CPU/Memória e gargalos de rede nos Traces, gerando alertas e criando Issues automaticamente no GitHub em caso de risco crítico.
3. **Agente de Testes Autônomo:** Avalia a telemetria gerada no processo de QA e disponibiliza um relatório executivo formatado em Markdown como artefato da pipeline.
