# Documentação das features de SMS

Este diretório foi adaptado diretamente para explicar os scripts de `../features_bibliotecas`, conforme solicitado. O documento usa os componentes do modelo institucional: capa, logos, cabeçalho, rodapé, caixas, tabelas e blocos de código.

- `main.tex`: documento principal.
- `main.pdf`: documento compilado.
- `config/dados.tex`: título e metadados.
- `capitulos/01-inicio.tex`: objetivo e mapa de leitura.
- `capitulos/02-recursos.tex`: bibliotecas, NLI, cálculo e fluxo compartilhado.
- `capitulos/03-features-semanticas.tex`: 19 features com hipóteses e resultados reais.
- `capitulos/04-features-estruturais.tex`: URL, encurtador, telefone, PIX e escrita.
- `capitulos/05-modulos-apoio.tex`: explicação dos dez módulos auxiliares.
- `capitulos/06-execucao-validacao.tex`: instalação, uso, resultados e limitações.
- `capitulos/07-referencias.tex`: fontes e manutenção.

## Compilar

Execute neste diretório:

```bash
make pdf
```

O alvo utiliza XeLaTeX. `make watch` recompila ao salvar. O conteúdo dos scripts Python não foi alterado para elaborar este documento. Os arquivos de prova e gabarito continuam separados do relatório principal.

## Escopo da validação

As tabelas de resultados reproduzem a execução registrada em 14/09/2026, com 27 acertos em 38 exemplos didáticos. A documentação foi elaborada em 15/09/2026. Não foi realizada nova avaliação do modelo para gerar o PDF.
