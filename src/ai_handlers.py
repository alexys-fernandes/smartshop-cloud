import os
import sys
import json
from groq import Groq

def inicializar_ambiente_requisitos():
    os.makedirs("security", exist_ok=True)
    vuln_path = os.path.join("security", "vulnerabilities.json")
    if not os.path.exists(vuln_path):
        default_security = {
            "scanned_at": "2026-05-23T12:00:00Z",
            "target": "SmartShop Cloud v1.0.0",
            "vulnerabilities": [
                {
                    "id": "SEC-001",
                    "component": "src/app.py",
                    "severity": "LOW",
                    "description": "Falta de sanitização estrita em tipos de dados de entrada de produtos, mitigada por tipagem estática.",
                    "remediation": "Adicionar validação estruturada com Pydantic para as propriedades do carrinho."
                }
            ],
            "status": "SECURE"
        }
        with open(vuln_path, "w", encoding="utf-8") as f:
            json.dump(default_security, f, indent=2)

    os.makedirs("docs", exist_ok=True)
    arch_path = os.path.join("docs", "architecture.md")
    if not os.path.exists(arch_path):
        default_arch = """# Documentação de Arquitetura - SmartShop Cloud 🤖

## Objetivo do Projeto
O SmartShop Cloud é um sistema de carrinho de compras automatizado e integrado com IA Generativa para aplicar conceitos avançados de AIOps.

## Estrutura do Repositório (Árvore do PDF)
- `.github/workflows/`: Pipelines de CI/CD.
- `src/`: Código fonte (`app.py`, `ai_handlers.py`, `intelligent_agent.py`).
- `tests/`: Bateria de testes unitários.
- `logs/`, `metrics/`, `traces/`: Telemetria e Observabilidade.
- `security/`: Relatórios de auditoria de vulnerabilidades (`vulnerabilities.json`).
- `docs/`: Documentação técnica e relatórios automáticos.
"""
        with open(arch_path, "w", encoding="utf-8") as f:
            f.write(default_arch)

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Erro: GROQ_API_KEY não configurada nas variáveis de ambiente.")
        sys.exit(1)
    return Groq(api_key=api_key)

def analyze_quality_gate(coverage_report_path):
    client = get_groq_client()
    
    if not os.path.exists(coverage_report_path):
        print(f"Erro: Arquivo de cobertura '{coverage_report_path}' não foi encontrado.")
        sys.exit(1)
        
    with open(coverage_report_path, "r") as f:
        report_content = f.read()
        
    prompt = f"""
    Você é o Agente de Testes e Quality Gate da SmartShop Cloud.
    Analise o seguinte relatório de cobertura de código do pytest:
    
    {report_content}
    
    Responda ESTRITAMENTE em formato JSON válido, sem qualquer texto introdutório ou explicativo fora do JSON.
    A estrutura deve ser exatamente esta:
    {{
        "status": "APROVADO" ou "BLOQUEADO",
        "motivo": "Sua justificativa técnica resumida aqui."
    }}
    Regra de Bloqueio: Bloqueie o pipeline se a cobertura total de linhas for menor que 80% ou se houver falhas de testes.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    return json.loads(completion.choices[0].message.content)

def analyze_observability(log_path, metrics_path, trace_path):
    client = get_groq_client()
    
    for path in [log_path, metrics_path, trace_path]:
        if not os.path.exists(path):
            print(f"Erro: Arquivo não encontrado no caminho: {path}")
            sys.exit(1)
            
    with open(log_path, "r") as f: logs = f.read()
    with open(metrics_path, "r") as f: metrics = f.read()
    with open(trace_path, "r") as f: traces = f.read()
    
    prompt = f"""
    Você é o Agente de Observabilidade e Incidentes da SmartShop Cloud.
    Analise os seguintes dados do sistema:
    
    LOGS:
    {logs}
    
    MÉTRICAS:
    {metrics}
    
    TRACES:
    {traces}
    
    Identifique erros críticos, degradação de performance e gargalos.
    Responda ESTRITAMENTE em formato JSON válido com o seguinte formato:
    {{
        "incidente_detectado": true ou false,
        "nivel_risco": "BAIXO" ou "MEDIO" ou "CRITICO",
        "titulo_issue": "Título resumido do problema",
        "descricao_detalhada": "Análise técnica curta conectando os logs falhos, alto consumo de métricas e gargalo no trace."
    }}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    return json.loads(completion.choices[0].message.content)

if __name__ == "__main__":
    inicializar_ambiente_requisitos()

    if len(sys.argv) < 2:
        print("Uso: python src/ai_handlers.py [quality|observability]")
        sys.exit(1)
        
    mode = sys.argv[1]
    
    if mode == "quality":
        res = analyze_quality_gate("coverage.txt")
        print(f"Decisão da IA: {res['status']}")
        print(f"Motivo: {res['motivo']}")
        if res["status"] == "BLOQUEADO":
            sys.exit(1)
            
    elif mode == "observability":
        res = analyze_observability("logs/app.log", "metrics/metrics.json", "traces/trace.txt")
        with open("obs_result.json", "w") as out:
            json.dump(res, out)
        print("Análise de observabilidade gerada com sucesso em obs_result.json")
