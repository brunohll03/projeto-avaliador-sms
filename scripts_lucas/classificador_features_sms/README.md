# Classificador de features de SMS

Extrai **24 características de mensagens SMS em português**, compara os valores com anotações existentes e gera um painel local para revisar as divergências. A versão recomendada está em **`notebook_features_final/`**.

São 23 features binárias (`0` ou `1`) e a carga emocional (`baixa`, `média` ou `alta`), acompanhada de sua proporção numérica. **O programa não classifica uma mensagem como golpe.** A coluna `possivel_golpe`, quando existe, é preservada da entrada.

## Requisitos

- Python **3.12**.
- Java **17 ou superior** para o LanguageTool local.
- VS Code com suporte a Python/Jupyter para abrir o notebook, ou execução pelo terminal.
- Internet para instalar as dependências e baixar o LanguageTool na primeira utilização sem cache. As mensagens são analisadas localmente; não se usa a API pública do corretor.

Confira as instalações:

```bash
python3 --version
java -version
```

## Instalação

Mantenha o diretório do repositório com o nome **`classificador_features_sms`**: os imports Python usam esse nome. Se o download do GitHub criar `classificador_features_sms-main`, renomeie a pasta.

Entre nessa pasta e execute no terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No Windows, substitua a ativação por `.venv\Scripts\Activate.ps1` no PowerShell e use `python` se `python3` não estiver disponível.

O `requirements.txt` da raiz encaminha para as versões registradas na versão final. As dependências das versões antigas são separadas.

## Executar pelo notebook

1. Abra `notebook_features_final/classificador_final_revisao.ipynb` no VS Code.
2. Em **Selecionar Kernel**, escolha o Python da `.venv` criada acima.
3. Clique em **Executar Tudo**. Após alterar scripts ou instalar bibliotecas, use **Reiniciar Kernel** antes de executar novamente.

O notebook usa como referência:

```text
dataset_estaticos/DATASET - Dataset_limpo_V1.csv
```

Para usar outra referência, altere a variável `fonte` na célula de carregamento. A verificação histórica do notebook compara a fonte original com seu manifesto quando o caminho coincide; arquivos históricos ausentes geram apenas aviso.

## Executar pelo terminal

Dentro da pasta `classificador_features_sms`:

```bash
python notebook_features_final/executar.py
```

Para outro CSV anotado e uma pasta de saída separada:

```bash
python notebook_features_final/executar.py --origem "caminho/referencia.csv" --saida "notebook_features_final/resultados/outro_dataset"
```

A referência deve ser um CSV UTF-8 separado por vírgulas, com `Mensagem` e as **24 colunas de features** listadas em [definicoes.json](notebook_features_final/definicoes.json). Rótulos binários devem ser `0` ou `1`; carga emocional aceita baixo/baixa, médio/média e alto/alta. Mensagens vazias ou repetidas são rejeitadas nesta rotina de comparação.

Esse comando exige uma referência **já anotada** para comparação. Para classificar uma mensagem sem gabarito, use a função `analisar_sms` descrita no [guia da versão final](notebook_features_final/README.md).

## Saídas e revisão humana

Os arquivos são gravados em `notebook_features_final/resultados/`:

| Arquivo | Conteúdo |
|---|---|
| `dataset_gerado.csv` | Mensagens e atributos calculados pelos scripts. |
| `comparacao_completa.csv` | Valores originais e gerados lado a lado. |
| `divergencias.csv` | Uma linha por **mensagem e feature** divergente. |
| `metricas_por_feature.csv` | Concordância por feature, sem assumir que o original está correto. |
| `revisao_divergencias.html` | Painel local com filtros e campos de revisão. |
| `revisao_humana.csv` | Divergências e decisões salvas. |
| `resultado_testes_sms.csv` | Resultados dos 144 SMS sintéticos, separados da referência. |
| `resumo_execucao.json` | Contagens, parâmetros e hashes da execução. |

Abra `revisao_divergencias.html` no navegador, registre as decisões e clique em **Baixar revisão CSV** antes de fechar. O download contém a revisão, **não um dataset corrigido**. Para continuar, importe esse CSV no painel. Para reaproveitá-lo na próxima execução do classificador, coloque-o como `resultados/revisao_humana.csv`.

Uma nova execução substitui as saídas geradas. Decisões sobre o mesmo texto, feature e par de valores são reaproveitadas; o CSV de revisão anterior é arquivado. Decisões que só estão na página aberta precisam ser baixadas primeiro. **A fonte original não é modificada e as decisões não são aplicadas automaticamente a ela.**

## Testes

Com a `.venv` ativa, vá para a pasta **que contém** `classificador_features_sms` e execute:

```bash
cd ..
python -m unittest classificador_features_sms.notebook_features_final.testes.test_integridade classificador_features_sms.notebook_features_final.testes.test_pedidos_informais classificador_features_sms.notebook_features_final.testes.test_senha_atualizacao classificador_features_sms.notebook_features_final.testes.test_auditoria_divergencias
```

Mantenha `tests/` da raiz, `notebook_features_final/testes/`, `resultados/analise_solicita_senha.csv` e `auditoria_divergencias_20260917/casos_revisados.json`: são usados nos testes. O `.gitignore` preserva essas referências.

Os 144 SMS sintéticos verificam uma feature-alvo por mensagem. São testes de desenvolvimento, não prova de precisão de 100% em mensagens reais. Consulte a [auditoria](notebook_features_final/auditoria_divergencias_20260917/RELATORIO.md) para conhecer correções e limitações.

## Estrutura

```text
classificador_features_sms/
├── README.md
├── requirements.txt
├── dataset_estaticos/         # referência anotada
├── notebook_features_final/  # versão recomendada
│   ├── features/             # regras específicas
│   ├── bibliotecas/          # integração com bibliotecas
│   ├── testes/               # casos sintéticos e regressões
│   ├── fontes/               # dicionário de features
│   └── resultados/           # arquivos gerados localmente
├── tests/                    # casos anteriores usados na regressão
├── features/                 # implementação inicial
└── features_bibliotecas/     # implementação anterior com bibliotecas
```

O [README da versão inicial](README_VERSAO_INICIAL.md) documenta os comandos antigos. Não confunda essas implementações com a versão final.

## Problemas comuns

- **`fg: job not found: pip`**: no terminal, use `python -m pip ...`, sem `%`. `%pip` é uma instrução de célula Jupyter.
- **`ModuleNotFoundError`**: instale as dependências na `.venv` e selecione esse mesmo ambiente no kernel do notebook.
- **Erro do Matplotlib após instalar/atualizar**: primeiro reinicie o kernel. Se persistir, confira se o kernel usa a `.venv`, evitando misturar bibliotecas de ambientes diferentes.
- **LanguageTool indisponível**: confira `java -version`, as dependências e o acesso à internet para o primeiro download. Falhas do corretor interrompem a execução; não são convertidas em “zero erros”.
- **Aviso de arquivos históricos ausentes**: é informativo; não exige restaurar versões antigas para classificar. Uma falha de integridade da fonte original é uma verificação diferente e deve ser investigada.

## Versionamento

O `.gitignore` exclui ambientes virtuais, caches, saídas regeneráveis, configurações locais e backups de execução. Não apaga arquivos do computador nem remove arquivos já versionados.

O dataset de entrada e os gabaritos necessários aos testes permanecem elegíveis para versionamento. Antes de publicar um repositório público, confira a autorização para compartilhar esses textos e remova as saídas salvas dos notebooks que contiverem mensagens reais. Ignorar CSVs gerados não remove conteúdo já incorporado em notebooks.
