const fs = require("fs");
const path = require("path");

const TAMANHO_ALVO = 1 * 1024 * 1024 * 1024; // 1GB
const SAIDA = path.join(__dirname, "data.txt");
const INTERVALO_CORINTHIANS = 25;

const palavrasFixas = [
  "cachorro", "gato", "carro", "estrada", "noite", "chuva",
  "amigo", "casa", "livro", "futebol", "sol", "tempo",
  "cidade", "praia", "computador", "janela", "festa", "trabalho",
  "dia", "noite", "pessoa", "amor", "vida", "tempo", "viagem"
];

function gerarFrase() {
  const palavrasNaFrase = Math.floor(Math.random() * 8) + 4;
  const palavras = Array.from({ length: palavrasNaFrase }, () => {
    return palavrasFixas[Math.floor(Math.random() * palavrasFixas.length)];
  });

  palavras[0] = palavras[0].charAt(0).toUpperCase() + palavras[0].slice(1);
  return palavras.join(" ") + ".\n";
}

function gerarArquivo() {
  const stream = fs.createWriteStream(SAIDA);
  let bytesEscritos = 0;
  let linhaAtual = 0;

  function escrever() {
    let ok = true;

    while (ok && bytesEscritos < TAMANHO_ALVO) {
      let linha;

      if (linhaAtual % INTERVALO_CORINTHIANS === 0) {
        linha = "Vai corinthians.\n";
      } else {
        linha = gerarFrase();
      }

      linhaAtual++;
      bytesEscritos += Buffer.byteLength(linha);
      ok = stream.write(linha);
    }

    if (bytesEscritos >= TAMANHO_ALVO) {
      stream.end();
      console.log("✅ Arquivo gerado: data.txt (~1GB), com frases e 'vai corinthians'.");
    } else {
      stream.once("drain", escrever);
    }
  }

  escrever();
}

gerarArquivo();
