#!/bin/zsh

set -eu

origem="${0:A:h}"
raiz="${origem:h}"

echo "Criar um projeto a partir do modelo LaTeX"
echo
read "nome?Nome da nova pasta: "

if [[ -z "${nome//[[:space:]]/}" ]]; then
  echo "O nome não pode ficar vazio."
  read "?Pressione Enter para fechar."
  exit 1
fi

destino="$raiz/$nome"

if [[ -e "$destino" ]]; then
  echo "Já existe um arquivo ou pasta com esse nome:"
  echo "$destino"
  read "?Pressione Enter para fechar."
  exit 1
fi

mkdir "$destino"
rsync -a \
  --exclude='main.pdf' \
  --exclude='prova.pdf' \
  --exclude='gabarito.pdf' \
  --exclude='*.aux' \
  --exclude='*.fdb_latexmk' \
  --exclude='*.fls' \
  --exclude='*.log' \
  --exclude='*.listing' \
  --exclude='*.out' \
  --exclude='*.synctex.gz' \
  --exclude='*.toc' \
  --exclude='*.xdv' \
  --exclude='criar-projeto.command' \
  "$origem/" "$destino/"

echo
echo "Projeto criado em:"
echo "$destino"
open "$destino"
read "?Pressione Enter para fechar."
