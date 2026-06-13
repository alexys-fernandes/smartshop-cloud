import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from groq import Groq

def encontrar_ultimo_trace(traces_dir: Path) -> list | None:
    arquivos = sorted(traces_dir.glob("canary_*.json"), reverse=True)
    if not arquivos:
        return None
    return json.loads(arquivos[0].read_text(encoding="utf-8"))

def detectar_necessidade_rollback(trace: list) -> tuple[bool, dict]:
    for fase in trace:
        if (fase.get("cpu_pct", 0) >= 80 or 
            fase.get("memory_pct", 0) >= 85 or 
            fase.get("error_rate_pct", 0) >= 5.0 or 
            fase.get("latency_ms", 0) >= 800):
            return True, fase
    return False, {}

def executar_rollback_producao() -> str:
    print("\n[ROLLBACK] Desfazendo alterações no tráfego da Cloud...")
    print("[ROLLBACK] Apontando DNS de volta para a última tag estável de Produção.")
    return datetime.now().isoformat()

def gerar_relatorio_sre(trace, metricas_falha, timestamp_rollback) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
Você é um Engenheiro de Confiabilidade de Sites (SRE).
Analise o seguinte incidente de deploy com falha no ecossistema smartshop-cloud e elabore um relatório técnico em português.

TRACE COMPLETO DO CANARY:
{json.dumps(trace, indent=2)}

MÉTRICAS DA FASE DE FALHA:
{json.dumps(metricas_falha, indent=2)}

HORÁRIO DO ROLLBACK AUTOMÁTICO: {timestamp_rollback}

Formate sua resposta usando os tópicos:
1. Resumo do Incidente
2. Causa Raiz Identificada
3. Impacto Estimado na SmartShop
4. Resposta e Ação de Recuperação Tomada
5. Recomendações Corretivas para o Time de Engenharia
"""
    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        max_completion_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content if 'response' in locals() else resposta.choices[0].message.content

def abrir_issue_github(titulo, corpo):
    """Cria uma Issue usando o gh CLI com fallback seguro (Regra de Boa Prática 4)."""
    cmd = ["gh", "issue", "create", "--title", titulo, "--body", corpo, "--label", "rollback,automated-alert"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"\n[GITHUB] Issue criada com sucesso: {result.stdout.strip()}")
        else:
            # Fallback quando gh CLI falha ou não está autenticado no ambiente local
            print("\n[FALLBACK BOAS PRÁTICAS] gh CLI retornou erro. Exibindo relatório localmente:")
            print(f"\nTítulo sugerido: {titulo}\n\n{corpo}")
    except FileNotFoundError:
        # Fallback quando o executável gh não existe na máquina do desenvolvedor
        print("\n[FALLBACK BOAS PRÁTICAS] Ferramenta 'gh' CLI não instalada localmente. Relatório de Erro:")
        print(f"\nTítulo sugerido: {titulo}\n\n{corpo}")

def main():
    raiz = Path(__file__).parent.parent
    traces_dir = raiz / "traces"
    
    trace = encontrar_ultimo_trace(traces_dir)
    if not trace:
        print("Nenhum histórico de canary localizado para analisar.")
        sys.exit(0)
        
    precisa_rollback, metricas_falha = detectar_necessidade_rollback(trace)
    if not precisa_rollback:
        print("Métricas operacionais dentro da normalidade. Nenhuma ação de rollback requerida.")
        sys.exit(0)
        
    timestamp = executar_rollback_producao()
    print("Gerando diagnóstico automatizado via IA (Groq)...")
    relatorio = gerar_relatorio_sre(trace, metricas_falha, timestamp)
    
    titulo_issue = f"[CRITICAL-ROLLBACK] Falha operacional detectada na Fase {metricas_falha.get('percentual_trafego')}% do Canary"
    corpo_issue = f"## Alerta de Rollback Automatizado\n\n{relatorio}\n\n*Relatório emitido pela IA de Observabilidade do Pipeline.*"
    
    abrir_issue_github(titulo_issue, corpo_issue)
    sys.exit(1)

if __name__ == "__main__":
    main()
