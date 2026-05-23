import os
import sys
from groq import Groq

def main():
    api_key = os.environ.get('GROQCLOUD_API_KEY')
    if not api_key:
        print("Erro: GROQCLOUD_API_KEY não configurada.")
        sys.exit(1)

    client = Groq(api_key=api_key)
    
    if not os.path.exists('coverage.txt'):
        print("Erro: Arquivo coverage.txt não encontrado.")
        sys.exit(1)

    with open('coverage.txt', 'r') as f:
        cov_data = f.read()
        
    prompt = f"""
    Você é o Agente de Testes da SmartShop Cloud. Sua função é avaliar a cobertura e gerar relatórios.
    Com base neste relatório de cobertura:
    {cov_data}

    Gere um relatório executivo formatado em Markdown para os desenvolvedores contendo:
    1. Resumo da cobertura atual.
    2. Avaliação de risco.
    3. Sugestão de melhoria ou parabenização caso esteja acima de 80%.
    """

    completion = client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.2
    )

    with open('relatorio_agente.md', 'w') as out:
        out.write(completion.choices[0].message.content)
    print("Relatório executivo gerado com sucesso em relatorio_agente.md!")

if __name__ == "__main__":
    main()
