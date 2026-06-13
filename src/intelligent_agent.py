import os
import sys
from groq import Groq

def main():
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("Erro: GROQ_API_KEY não configurada.")
        sys.exit(1)

    client = Groq(api_key=api_key)
    
    if not os.path.exists('coverage.txt'):
        print("Erro: Arquivo coverage.txt não encontrado.")
        sys.exit(1)

    with open('coverage.txt', 'r') as f:
        cov_data = f.read()
        
    prompt = f"""
    Você é o Agente de Testes e Documentação da SmartShop Cloud. Sua função é avaliar a cobertura e gerar relatórios executivos.
    Com base neste relatório de cobertura:
    {cov_data}

    Gere um relatório executivo formatado em Markdown para os desenvolvedores contendo:
    1. Resumo analítico da cobertura atual.
    2. Avaliação técnica de risco operacional.
    3. Sugestão prática de melhoria ou parabenização caso esteja acima de 80%.
    """

    completion = client.chat.completions.create(
        model='llama-3.1-8b-instant',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.2
    )

    os.makedirs('docs', exist_ok=True)
    
    relatorio_path = os.path.join('docs', 'relatorio_agente.md')
    with open(relatorio_path, 'w', encoding='utf-8') as out:
        out.write(completion.choices[0].message.content)
        
    print(f"Relatório executivo gerado com sucesso em {relatorio_path}!")

if __name__ == "__main__":
    main()
