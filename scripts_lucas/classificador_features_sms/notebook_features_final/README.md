# Versão final do classificador de SMS

Para instalar Python, Java, dependências e escolher o kernel, siga o [guia principal](../README.md). Os comandos de terminal abaixo partem da pasta `classificador_features_sms`.

## Executar

```bash
python notebook_features_final/executar.py
```

Ou abra `classificador_final_revisao.ipynb`, selecione a `.venv` e execute as células em ordem. O notebook não instala Java. A primeira utilização do LanguageTool sem cache pode baixar seu servidor local.

## Classificar uma mensagem sem gabarito

Na pasta **que contém** `classificador_features_sms`, com a `.venv` ativa:

```python
from classificador_features_sms.notebook_features_final.classificador import analisar_sms

resultado = analisar_sms("Informe seu CPF para continuar.")
print(resultado["features"])
print(resultado["detalhes"])
```

A função usa LanguageTool local, além das regras e bibliotecas. A referência anotada só é necessária para o fluxo de comparação, não para essa chamada.

## Bibliotecas e regras

- `phonenumbers`: valida formatos de telefone brasileiro com exclusões de identificadores.
- `linkify-it-py`: extrai URLs; o domínio é validado e comparado com a lista fixa de encurtadores.
- `regex` e `re`: reconhecem termos e relações locais entre ação, objeto e negação.
- `language-tool-python`: executa o LanguageTool pt-BR local; filtros separam erros aceitos e alertas ignorados.
- `pandas` e `numpy`: carregam dados, comparam rótulos e calculam medidas.
- `matplotlib`: produz gráficos no notebook.

As regras foram orientadas pelo [Dicionário de Features](fontes/Dicionario_de_Features.pdf). Não são um modelo treinado para reproduzir os rótulos originais. `possivel_golpe` é preservado, não previsto.

## Carga emocional

A proporção de palavras do léxico emocional é exportada junto da categoria. Os limites estão congelados em `configuracao_emocao.json`: baixa ≤ 1/17; média > 1/17 e ≤ 1/14; alta > 1/14. São tercis das proporções positivas no corpus de referência, sem usar seus rótulos categóricos. Zero fica em baixa.

Não recalcular esses limites a cada lote. Essa é uma medida lexical relativa, não uma avaliação psicológica; ironia, negação e contexto têm cobertura limitada.

## Revisar divergências

1. Execute o classificador para gerar `resultados/revisao_divergencias.html`.
2. Abra esse arquivo no navegador e filtre por feature, mensagem ou situação.
3. Registre `original`, `gerado`, `outro` ou `inconclusivo`. Para `outro`, informe o valor decidido.
4. Clique em **Baixar revisão CSV** para salvar. Decisões na página não são salvas automaticamente ao fechá-la.
5. Importe o CSV para continuar no painel. Para reutilizá-lo na execução seguinte, coloque-o em `resultados/revisao_humana.csv`.

O CSV exportado contém decisões de revisão. Não representa o dataset completo corrigido. A fonte nunca é alterada automaticamente. Cada divergência representa uma feature de uma mensagem; um SMS pode gerar várias linhas.

## Artefatos e histórico

- `resultados/dataset_gerado.csv`: atributos calculados pelos scripts.
- `resultados/resumo_execucao.json`: números e hashes da execução mais recente.
- `testes/sms_teste.csv`: 144 casos sintéticos; cada um tem gabarito para uma feature-alvo.
- `REVISAO_DAS_FEATURES.md`: revisão inicial, preservada como histórico.
- `auditoria_divergencias_20260917/RELATORIO.md`: auditoria posterior, com justificativas e limitações.

Na auditoria de 17/09/2026 foram registradas 3.757 divergências em 32.328 comparações (88,38% de concordância), com 144/144 testes sintéticos. Esses números são históricos; consulte o resumo da sua execução. Concordância com anotações não equivale a acurácia.

O `.gitignore` não distribui os resultados e backups locais. O notebook de auditoria histórica e seu gerador de relatórios exigem esses resultados arquivados; o notebook principal e o classificador não dependem deles. Os dois gabaritos de regressão externos à pasta `testes` continuam versionáveis e não devem ser apagados.

## Alterar regras

Edite `features/<nome>.py`; mudanças em `regras.py` podem afetar várias features. Acrescente exemplos positivos e negativos aos testes e execute a suíte descrita no README principal. Reinicie o kernel antes de reexecutar o notebook para carregar os módulos alterados. Não mude o gabarito apenas para fazer um teste passar.
