import redis
import json
import re
import os
from pathlib import Path

def mapper(input_file):
    # Cria a pasta "intermediate" se não existir
    if not os.path.isdir('intermediate'):
        Path('intermediate').mkdir(parents=True, exist_ok=True)
        
    # Conecta ao Redis
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    # Lista para armazenar as ocorrências de palavras
    word_occurrences = []

    # Processa o arquivo de entrada
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            for word in re.findall(r'\b[a-zA-Z]+\b', line.lower()):
                word_occurrences.append({word: 1})
    
    # Envia os dados para o Redis
    redis_key = f"mapper_{Path(input_file).stem}"
    redis_client.set(redis_key, json.dumps(word_occurrences))

    # Cria o arquivo JSON na pasta "intermediate"
    output_file = f'intermediate/{Path(input_file).stem}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(word_occurrences, f, ensure_ascii=False, indent=4)
        
    print(f"Mapper: processando {input_file}")

if __name__ == '__main__':
    # Exemplo de uso
    input_file = "data/input.txt"  # Substitua pelo caminho do arquivo de entrada
    mapper(input_file)
