import sys
import os


sys.path.append(os.path.abspath('./utils'))

from utils import mapper, shuffle, reducer
import multiprocessing
import json
from collections import defaultdict

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

def combine_results(output_dir='./output', result_file='./result.txt'):
    """Combina os resultados dos arquivos reduced_X_output.json e gera result.txt."""
    if not os.path.isdir(output_dir):
        print("A pasta 'output' não existe ou está vazia.")
        return

    combined_counts = defaultdict(int)


    for file in os.listdir(output_dir):
        if file.endswith('_output.json'):
            with open(os.path.join(output_dir, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for word, count in data.items():
                    combined_counts[word] += count

    with open(result_file, 'w', encoding='utf-8') as f:
        for word, total_count in combined_counts.items():
            f.write(f"{word}:{total_count}\n")

    print(f"Arquivo de resultados gerado: {result_file}")

def main():
    """Função principal para executar o pipeline MapReduce."""
    chunk_dir = './chunks'
    num_chunks = 10


    chunks = verify_chunks(chunk_dir, num_chunks)

 
    run_mapper(chunks)

   
    print("Executando o shuffle...")
    shuffle.shuffle()

    print("Executando o reducer...")
    reducer.reducer()

    
    print("Combinando os resultados...")
    combine_results()

    print("MapReduce completo")

if __name__ == "__main__":
    main()
