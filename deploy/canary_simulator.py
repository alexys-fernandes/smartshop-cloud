# deploy/canary_simulator.py
import time
import json
from pathlib import Path
from datetime import datetime
import sys

def carregar_metricas(arquivo: Path) -> dict:
    """Carrega métricas geradas pelos testes de estresse ou monitoramento simulado."""
    if arquivo.exists():
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        # Fallback caso o arquivo não exista localmente durante a simulação
        dados = {"cpu": 45, "memory": 60, "latency_ms": 250, "error_rate": 0.5}
        
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_pct": dados.get("cpu", 0),
        "memory_pct": dados.get("memory", 0),
        "latency_ms": dados.get("latency_ms", 0),
        "error_rate_pct": dados.get("error_rate", 0)
    }

def avaliar_fase(metricas: dict) -> bool:
    """Valida os thresholds de Canary definidos para o smartshop-cloud."""
    return (
        metricas["cpu_pct"] < 80 and
        metricas["memory_pct"] < 85 and
        metricas["error_rate_pct"] < 5.0 and
        metricas["latency_ms"] < 800
    )

def executar_canary(arquivo_metricas: Path, salvar_em: Path = None):
    fases = [10, 50, 100]
    historico = []
    print("\n=== INICIANDO CANARY DEPLOY - SMARTSHOP CLOUD ===\n")
    
    for percentual in fases:
        print(f"-> Promovendo tráfego para {percentual}%: Monitorando estabilidade...")
        time.sleep(1)
        
        metricas = carregar_metricas(arquivo_metricas)
        metricas["percentual_trafego"] = percentual
        passou = avaliar_fase(metricas)
        metricas["fase_aprovada"] = passou
        historico.append(metricas)
        
        status = "OK" if passou else "FALHA TIMEOUT/THRESHOLDS"
        print(f"   CPU: {metricas['cpu_pct']}% | Mem: {metricas['memory_pct']}% | Erros: {metricas['error_rate_pct']}% | Latência: {metricas['latency_ms']}ms -> [{status}]")
        
        if not passou:
            print(f"\n[ALERTA] Instabilidade na fase de {percentual}%. Abortando e acionando Rollback!")
            if salvar_em:
                salvar_em.write_text(json.dumps(historico, indent=2))
            return False, historico
            
        print(f"   Fase de {percentual}% bem-sucedida. Avançando...\n")
        
    print("=== DEPLOY CANARY 100% CONCLUÍDO COM SUCESSO ===")
    if salvar_em:
        # Regra de Boa Prática 6: Salvar traces em arquivos JSON com timestamp para auditoria
        salvar_em.write_text(json.dumps(historico, indent=2))
    return True, historico

if __name__ == "__main__":
    raiz = Path(__file__).parent.parent
    
    # Cria pasta de métricas e traces se não existirem
    (raiz / "metrics").mkdir(exist_ok=True)
    (raiz / "traces").mkdir(exist_ok=True)
    
    arquivo_metricas = raiz / "metrics" / "system-current.json"
    saida_trace = raiz / "traces" / f"canary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    sucesso, _ = executar_canary(arquivo_metricas=arquivo_metricas, salvar_em=saida_trace)
    print(f"\nTrace de auditoria salvo em: {saida_trace}")
    sys.exit(0 if sucesso else 1)
