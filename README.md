# MapReduce
## ✅ Pré-requisitos

- Python 3.8+
- Redis Server
- Bibliotecas Python: `redis`
  
### Instalação do Redis (Linux)

sudo apt update
sudo apt install redis
sudo systemctl start redis
sudo systemctl enable redis

## ⚙️ Configuração e Execução

### 1. Clonar o repositório e instalar dependências

```bash
git clone <url-do-repositório>
cd <pasta-do-projeto>
pip install redis
```

### 2. Gerar um arquivo grande de palavras aleatórias (1GB) e dividi-lo em 10 partes

Você pode criar esse arquivo assim:

```bash
node ./criaArquivo.js
node ./dividirArquivo.js
```

### 4. Rodar o coordenador

aqui ele vai coodernador

```bash
python3 main.py
```
## 🧪 Resultado Final

O resultado final é gerado no arquivo:

```
result.txt
```

Cada linha contém a contagem de uma palavra no estilo:

```
palavra1: 1500
palavra2: 2340
...
```
