import redis
import json
import re
import os
from pathlib import Path

# Cria a pasta "chunks"

def mapper(input_file):

    if not os.path.isdir('intermediate'):
        Path('intermediate').mkdir(parents=True, exist_ok=True)
        
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    word_occurrences = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            for word in re.findall(r'\b[a-zA-Z]+\b', line.lower()):
                # Adiciona cada ocorrência de uma palavra como uma entrada separada
                word_occurrences.append({word: 1})
    
    # Envia os dados para o Redis
    redis_client.rpush('shuffle_queue', json.dumps(word_occurrences))

    # Cria o arquivo JSON na pasta "intermediate"
    with open(f'intermediate/{Path(input_file).stem}.json', 'w', encoding='utf-8') as f:
        json.dump(word_occurrences, f, ensure_ascii=False, indent=4)
        
    print(f"Mapper: processando {input_file}")

if __name__ == '__main__':
    mapper()
