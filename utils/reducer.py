import json
import os
from pathlib import Path

def reducer():
    # Cria a pasta 'output' se não existir
    if not os.path.isdir('output'):
        Path('output').mkdir(parents=True, exist_ok=True)
    
    # Verifica se a pasta 'shuffled' existe
    if not os.path.isdir('shuffled'):
        print("A pasta 'shuffled' não existe ou está vazia.")
        return

    # Processa cada arquivo na pasta 'shuffled'
    for file in os.listdir('shuffled'):
        if file.endswith('_input.json'):  # Verifica se o arquivo é do tipo esperado
            with open(f'shuffled/{file}', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Soma os valores das listas
            reduced_data = {word: sum(counts) for word, counts in data.items()}
            
            # Cria o arquivo de saída na pasta 'output'
            output_file = f"output/{file.replace('_input.json', '_output.json')}"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(reduced_data, f, ensure_ascii=False, indent=4)
    
    print("Etapa reducer concluída. Arquivos gerados na pasta 'output'.")

if __name__ == "__main__":
    reducer()