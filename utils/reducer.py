import json
import redis
import os
from pathlib import Path

def reducer(redis_client):
    # Cria a pasta 'output' se não existir
    if not os.path.isdir('output'):
        Path('output').mkdir(parents=True, exist_ok=True)
    
    # Recupera as chaves do Redis que correspondem aos dados do shuffle
    keys = redis_client.keys('reduce_*')
    if not keys:
        print("Nenhuma chave correspondente encontrada no Redis para o reducer.")
        return

    # Processa cada chave no Redis
    for key in keys:
        # Decodifica a chave de bytes para string
        key_str = key.decode('utf-8')
        
        # Recupera os dados do Redis
        data = json.loads(redis_client.get(key))
        
        # Soma os valores das listas
        reduced_data = {word: sum(counts) for word, counts in data.items()}
        
        # Salva os resultados reduzidos no Redis com a chave correspondente
        reduced_key = key_str.replace('reduce_', 'reduced_')
        redis_client.set(reduced_key, json.dumps(reduced_data))
        
        # Salva os resultados reduzidos em um arquivo na pasta 'output'
        output_file = f'output/{reduced_key}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reduced_data, f, ensure_ascii=False, indent=4)
    
    print("Etapa reducer concluída. Resultados armazenados no Redis e na pasta 'output'.")

if __name__ == "__main__":
    # Exemplo de uso com Redis
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    reducer(redis_client)
