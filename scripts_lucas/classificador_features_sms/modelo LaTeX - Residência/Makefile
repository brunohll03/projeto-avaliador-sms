.DEFAULT_GOAL := pdf

.PHONY: pdf guia prova gabarito avaliacao watch watch-prova watch-gabarito open open-prova open-gabarito clean help

pdf:
	latexmk -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error main.tex

guia: pdf

prova:
	latexmk -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error prova.tex

gabarito:
	latexmk -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error gabarito.tex

avaliacao: prova gabarito

watch:
	latexmk -xelatex -synctex=1 -pvc -view=none -interaction=nonstopmode main.tex

watch-prova:
	latexmk -xelatex -synctex=1 -pvc -view=none -interaction=nonstopmode prova.tex

watch-gabarito:
	latexmk -xelatex -synctex=1 -pvc -view=none -interaction=nonstopmode gabarito.tex

open:
	open main.pdf

open-prova:
	open prova.pdf

open-gabarito:
	open gabarito.pdf

clean:
	latexmk -c main.tex
	latexmk -c prova.tex
	latexmk -c gabarito.tex
	rm -f capitulos/*.aux avaliacao/*.aux *.listing

help:
	@echo "make ou make pdf   - compila o guia/relatório (main.pdf)"
	@echo "make prova         - compila a prova (prova.pdf)"
	@echo "make gabarito      - compila o gabarito (gabarito.pdf)"
	@echo "make avaliacao     - compila prova e gabarito"
	@echo "make watch         - observa main.tex"
	@echo "make watch-prova   - observa prova.tex"
	@echo "make watch-gabarito - observa gabarito.tex"
	@echo "make open-prova / open-gabarito - abre o PDF correspondente"
	@echo "make clean         - remove arquivos auxiliares"
