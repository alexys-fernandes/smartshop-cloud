import json
import sys
from pathlib import Path
from groq import Groq

def carregar_contexto(raiz: Path) -> dict:
    """Lê os artefatos de cobertura e logs do projeto smartshop-cloud."""
    contexto = {}
    
    # Adaptado para ler a cobertura gerada pelo Jest no Node.js
    # Procurando pelo arquivo gerado pelo Jest (coverage-summary.json ou coverage.json)
    coverage_path = raiz / "coverage" / "coverage-summary.json"
    if not coverage_path.exists():
        # Fallback para coverage.json na raiz ou pasta coverage
        coverage_path = raiz / "coverage" / "coverage.json"
        
    if coverage_path.exists():
        try:
            dados = json.loads(coverage_path.read_text(encoding="utf-8"))
            # O Jest summary costuma estruturar por {"total": {"lines": {"pct": 85}}}
            if "total" in dados and "lines" in dados["total"]:
                contexto["cobertura_pct"] = dados["total"]["lines"].get("pct", 0)
            elif "totals" in dados: # Formato genérico
                contexto["cobertura_pct"] = dados.get("totals", {}).get("percent_covered", 0)
            else:
                contexto["cobertura_pct"] = 0
        except Exception:
            contexto["cobertura_pct"] = 0
    else:
        # Se não achar o JSON, define 0 para forçar validação via logs ou rejeição segura
        contexto["cobertura_pct"] = 0

    # Ler logs da aplicação na pasta logs/
    log_path = raiz / "logs"
    if log_path.exists():
        logs = []
        for arquivo in log_path.glob("*.log"):
            try:
                conteudo = arquivo.read_text(encoding="utf-8", errors="ignore")
                logs.append(f"Arquivo: {arquivo.name}\n{conteudo[:500]}")
            except Exception as e:
                logs.append(f"Erro ao ler {arquivo.name}: {str(e)}")
        contexto["logs"] = "\n\n--\n\n".join(logs) if logs else "sem logs"
    else:
        contexto["logs"] = "sem logs"
        
    return contexto

def rodar_deploy_gate(raiz: Path) -> str:
    """Consulta o Groq usando temperatura 0 e limpa o Markdown da resposta."""
    ctx = carregar_contexto(raiz)
    
    prompt = f"""
Você é um engenheiro DevOps sênior responsável pelo projeto smartshop-cloud (Node.js/TypeScript).
Sua tarefa é decidir se este build pode ser promovido para produção.

REGRAS OBRIGATÓRIAS:
1. Se a cobertura de testes for menor que 80%, responda BLOCK.
2. Se os logs indicarem falhas críticas de banco de dados (MongoDB/PostgreSQL), indisponibilidade de serviços externos ou erros não tratados na API, responda BLOCK.
3. Caso contrário, responda APPROVE.

Cobertura de testes atual: {ctx["cobertura_pct"]:.1f}%
Logs coletados: {ctx["logs"]}

Retorne APENAS um JSON válido no formato abaixo, sem qualquer texto explicativo fora do JSON:
{{
  "decision": "APPROVE",
  "reason": "explicação curta",
  "risk_score": 10
}}
ou
{{
  "decision": "BLOCK",
  "reason": "explicação curta",
  "risk_score": 90
}}
"""
    client = Groq()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,  # Regra de Boa Prática 2: Resposta determinística
        max_completion_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    
    texto = response.choices[0].message.content.strip()
    
    # Regra de Boa Prática 3: Remover blocos markdown da resposta antes do json.loads
    texto = texto.replace("```json", "").replace("```", "").strip()
    
    try:
        resultado = json.loads(texto)
    except json.JSONDecodeError:
        print("[Deploy Gate] Erro crítico ao interpretar resposta da IA:", texto)
        return "BLOCK"
        
    print(f"Decision   : {resultado['decision']}")
    print(f"Reason     : {resultado['reason']}")
    print(f"Risk Score : {resultado['risk_score']}/100")
    return resultado["decision"]

if __name__ == "__main__":
    raiz = Path(__file__).parent.parent
    decisao = rodar_deploy_gate(raiz)
    sys.exit(0 if decisao == "APPROVE" else 1)
