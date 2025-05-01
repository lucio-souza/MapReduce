import json
import os
from pathlib import Path

def shuffle():
    # Cria a pasta 'shuffled' se não existir
    if not os.path.isdir('shuffled'):
        Path('shuffled').mkdir(parents=True, exist_ok=True)
    
    # Verifica se a pasta 'intermediate' existe
    if not os.path.isdir('intermediate'):
        print("A pasta 'intermediate' não existe ou está vazia.")
        return
    
    # Lê todos os arquivos .json na pasta 'intermediate'
    for file in os.listdir('intermediate'):
        if file.endswith('.json'):
            combined_counts = {}  # Dicionário para armazenar as contagens combinadas para o arquivo atual
            
            with open(f'intermediate/{file}', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Processa cada dicionário na lista
                for entry in data:
                    for word, count in entry.items():
                        if word not in combined_counts:
                            combined_counts[word] = []
                        combined_counts[word].append(count)

            # Salva o resultado em um arquivo correspondente na pasta 'shuffled'
            output_file = f'shuffled/reduce_{Path(file).stem.split("chunk")[-1]}_input.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(combined_counts, f, ensure_ascii=False, indent=4)
    
    print('Processo de shuffle concluído')

if __name__ == '__main__':
    shuffle()