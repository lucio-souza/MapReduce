import sys
import os
import json
import multiprocessing
from collections import defaultdict
import redis

sys.path.append(os.path.abspath('./utils'))

from utils import mapper, shuffle, reducer

# Configuração do Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def verify_chunks(chunk_dir, num_chunks):
    """Verifica se todos os arquivos chunkX.txt existem na pasta chunks."""
    chunks = [os.path.join(chunk_dir, f'chunk{i}.txt') for i in range(num_chunks)]
    for chunk in chunks:
        if not os.path.exists(chunk):
            print(f"Arquivo {chunk} não encontrado.")
            sys.exit(1)
    return chunks

def run_mapper(chunks):
    """Executa o mapper em paralelo para os arquivos chunks."""
    print("Executando o mapper...")
    with multiprocessing.Pool(processes=len(chunks)) as pool:
        pool.map(mapper.mapper, chunks)

def combine_results(result_file='./result.txt'):
    """Combina os resultados armazenados no Redis e gera result.txt."""
    combined_counts = defaultdict(int)

    # Recupera os resultados do Redis
    keys = redis_client.keys('reduce_*')
    for key in keys:
        data = json.loads(redis_client.get(key))
        for word, counts in data.items():
            combined_counts[word] += sum(counts)

    # Salva os resultados combinados em um arquivo
    with open(result_file, 'w', encoding='utf-8') as f:
        for word, total_count in combined_counts.items():
            f.write(f"{word}:{total_count}\n")

    print(f"Arquivo de resultados gerado: {result_file}")

def main():
    """Função principal para executar o pipeline MapReduce."""
    chunk_dir = './chunks'
    num_chunks = 10

    # Verifica os arquivos de entrada
    chunks = verify_chunks(chunk_dir, num_chunks)

    # Executa o mapper
    run_mapper(chunks)

    # Executa o shuffle
    print("Executando o shuffle...")
    shuffle.shuffle(redis_client)

    # Executa o reducer
    print("Executando o reducer...")
    reducer.reducer(redis_client)

    # Combina os resultados
    print("Combinando os resultados...")
    combine_results()

    print("MapReduce completo")

if __name__ == "__main__":
    main()
