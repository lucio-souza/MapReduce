const fs = require("fs");
const path = require("path");
const readline = require("readline");

const arquivoFonte = path.join(__dirname, "data.txt");
const pastaSaida = path.join(__dirname, "chunks");
const numChunks = 10;

// Garante que a pasta "chunks/" existe
if (!fs.existsSync(pastaSaida)) {
  fs.mkdirSync(pastaSaida);
}

// 1️⃣ Passo: Conta o número total de linhas
async function contarLinhas() {
  const arquivo = fs.createReadStream(arquivoFonte);
  const rl = readline.createInterface({ input: arquivo });

  let linhas = 0;
  for await (const _ of rl) {
    linhas++;
  }
  return linhas;
}

// 2️⃣ Passo: Divide as linhas igualmente entre os chunks
async function dividirArquivo() {
  const totalLinhas = await contarLinhas();
  const linhasPorChunk = Math.ceil(totalLinhas / numChunks);

  const arquivo = fs.createReadStream(arquivoFonte);
  const rl = readline.createInterface({ input: arquivo });

  let atualChunk = 0;
  let contadorLinha = 0;
  let escritor = fs.createWriteStream(path.join(pastaSaida, `chunk${atualChunk}.txt`));

  for await (const linha of rl) {
    if (contadorLinha >= linhasPorChunk) {
      escritor.end();
      atualChunk++;
      contadorLinha = 0;
      escritor = fs.createWriteStream(path.join(pastaSaida, `chunk${atualChunk}.txt`));
    }

    escritor.write(linha + "\n");
    contadorLinha++;
  }

  escritor.end();
  console.log("✅ Arquivo dividido em 10 partes na pasta 'chunks/'");
}

dividirArquivo();
