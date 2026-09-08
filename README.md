# Classificador de Golpes em SMS

Projeto de Machine Learning desenvolvido para analisar mensagens SMS e estimar a probabilidade de uma mensagem representar um possível golpe.

A solução utiliza características relacionadas a engenharia social, persuasão, solicitações de informações, urgência, ameaças, URLs, pagamentos e outros padrões presentes nas mensagens.

O resultado será apresentado como uma estimativa de risco, não como uma confirmação de fraude.

## Tecnologias

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Jupyter Notebook
* Joblib
* Streamlit

## Estrutura

```text
projeto_sms_golpes/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_exploracao.ipynb
│   ├── 02_preparacao.ipynb
│   ├── 03_modelagem.ipynb
│   ├── 04_preparacao.ipynb
│   ├── 05_modelagem.ipynb
│   ├── 06_preparacao_embb.ipynb
│   ├── 07_modelagem_embb.ipynb
│   ├── 08_avaliacao_embb.ipynb
│   ├── 09_nao_supervisionado.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train.py
│   ├── predict.py
│   └── risk.py
│
├── models/
├── app/
│   └── app.py
│
├── reports/
│   └── figures/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Instalação

Criar o ambiente virtual:

```bash
py -m venv .venv
```

Ativar no Windows:

```powershell
usually quick a declare music..venv\Scripts\Activate.ps1
```

Instalar as dependências:

```bash
pip install -r requirements.txt
```

## Objetivo

O modelo deverá aprender padrões presentes nas características das mensagens e utilizá-los para classificar novas mensagens como:

* Não golpe
* Possível golpe

Além da classificação, o sistema deverá apresentar uma probabilidade estimada e um nível de risco.

## Observação

A probabilidade produzida pelo modelo representa uma estimativa baseada nos dados utilizados durante o treinamento. O resultado não deve ser interpretado como uma confirmação de fraude.


## Modelo supervisionado

### 1. Preparação dos dados

* Definição da variável-alvo `Possivel golpe`.
* Separação entre dados textuais e características estruturadas.
* Divisão dos dados em treinamento e teste, utilizando estratificação.

### 2. Processamento das mensagens

* Normalização dos textos.
* Transformação das mensagens utilizando **TF-IDF**.
* Combinação das características textuais com **24 features estruturadas** relacionadas a sinais de possíveis golpes.

### 3. Modelagem com TF-IDF

Foram treinados e comparados cinco algoritmos de classificação:

* Logistic Regression
* Multinomial Naive Bayes
* LinearSVC
* Random Forest
* XGBoost

### 4. Avaliação dos modelos

Os modelos foram avaliados utilizando:

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC
* Curva ROC
* Matriz de Confusão
* Falsos positivos e falsos negativos
* Diferentes valores de **threshold**

### 5. Experimento com Embeddings

Como experimento adicional, foi avaliada uma segunda abordagem para representação das mensagens utilizando **Embeddings**.

Foi utilizado o modelo:

`paraphrase-multilingual-MiniLM-L12-v2`

Os embeddings foram combinados com as mesmas **24 features estruturadas** utilizadas na abordagem TF-IDF.

Foram avaliados quatro algoritmos:

* Logistic Regression
* LinearSVC
* Random Forest
* XGBoost

O objetivo foi verificar se uma representação semântica das mensagens poderia apresentar resultados superiores ao TF-IDF.

### 6. Comparação entre TF-IDF e Embeddings

A comparação foi realizada utilizando o **XGBoost**, que apresentou os melhores resultados entre os modelos avaliados em cada abordagem.

| Métrica          | XGBoost + TF-IDF (30%) | XGBoost + Embeddings (40%) |
| ---------------- | ---------------------: | -------------------------: |
| Accuracy         |             **97,78%** |                     97,04% |
| Precision        |                 96,19% |                 **97,03%** |
| Recall           |             **98,06%** |                     95,15% |
| F1-score         |             **97,12%** |                     96,08% |
| ROC-AUC          |                 0,9953 |                 **0,9969** |
| Falsos positivos |                      4 |                      **3** |
| Falsos negativos |                  **2** |                          5 |

Embora a abordagem com **Embeddings** tenha apresentado um ROC-AUC ligeiramente superior e menos falsos positivos, a abordagem **TF-IDF** apresentou melhor **Recall** e **F1-score**, além de menor quantidade de falsos negativos.

Considerando o objetivo principal do projeto, que é **identificar possíveis golpes e reduzir o risco de classificá-los incorretamente como mensagens legítimas**, foi escolhido o:

> **XGBoost + TF-IDF com threshold de 30%**

Essa configuração identificou **101 dos 103 possíveis golpes**, resultando em apenas **2 falsos negativos**.

### 7. Análise das características

Após a escolha do modelo final, foram analisadas as características utilizadas pelo XGBoost:

* Importância das features.
* Frequência dos principais sinais presentes nas mensagens.
* Principais características utilizadas pelo modelo na classificação.
* Relação entre os sinais estruturados e a classificação de possível golpe.

### 8. Análise de erros

Foi realizada uma análise individual dos erros do modelo, com foco principalmente nos **falsos negativos**.

Foram investigados:

* Mensagens classificadas incorretamente como não golpe.
* Características presentes nessas mensagens.
* Possíveis padrões que dificultaram a identificação.
* Oportunidades de melhoria do modelo.

### 9. Protótipo

Por fim, o modelo selecionado será utilizado em um **protótipo de classificação de SMS**, permitindo testar novas mensagens e apresentar a classificação realizada pelo modelo.

---

## Fluxograma

```text
                    DATASET PRONTO
                          │
                          ↓
                     EXPLORAÇÃO
                          │
                          ↓
                  GRÁFICOS / ANÁLISE
                          │
                          ↓
                   TARGET: GOLPE
                          │
                          ↓
                    TREINO / TESTE
                          │
                          ↓
                ┌─────────────────────┐
                │ PROCESSAMENTO TEXTO │
                └─────────────────────┘
                          │
              ┌───────────┴───────────┐
              ↓                       ↓
           TF-IDF                 EMBEDDINGS
              │                       │
              ↓                       ↓
       + 24 FEATURES           + 24 FEATURES
              │                       │
              ↓                       ↓
        5 MODELOS                 4 MODELOS
              │                       │
              ↓                       ↓
          AVALIAÇÃO                AVALIAÇÃO
              │                       │
              ↓                       ↓
       MÉTRICAS + ROC          MÉTRICAS + ROC
       MATRIZ DE CONFUSÃO     MATRIZ DE CONFUSÃO
              │                       │
              ↓                       ↓
          THRESHOLDS              THRESHOLDS
              │                       │
              └───────────┬───────────┘
                          ↓
                  COMPARAÇÃO FINAL
                          │
                          ↓
                 TF-IDF × EMBEDDINGS
                          │
                          ↓
                   ESCOLHA FINAL
                          │
                          ↓
              XGBOOST + TF-IDF
               THRESHOLD 30%
                          │
                          ↓
                  ANÁLISE DE ERROS
                          │
                          ↓
                     PROTÓTIPO
```
### Modelo não supervisionado

O aprendizado não supervisionado foi utilizado como um experimento complementar ao modelo supervisionado, com o objetivo de investigar se as mensagens do dataset apresentam padrões ou agrupamentos naturais, sem utilizar a variável-alvo Possivel golpe durante o treinamento.


### 1. Preparação dos dados

Utilização das mensagens já preparadas no dataset.
Seleção da coluna Mensagem para análise textual.
Normalização dos textos.
Separação da variável Possivel golpe, que não é utilizada durante o treinamento do algoritmo não supervisionado.

### 2. Representação das mensagens

As mensagens foram transformadas em representações numéricas utilizando Embeddings.

Foi utilizado o modelo:

paraphrase-multilingual-MiniLM-L12-v2

Essa abordagem transforma cada mensagem em um vetor numérico capaz de representar características semânticas do texto.

O processo pode ser representado como:

Mensagem
    ↓
Normalização
    ↓
Embeddings
    ↓
Vetores numéricos

### 3. Agrupamento com K-Means

Foi utilizado o algoritmo K-Means, uma técnica de aprendizado não supervisionado baseada em agrupamento (clustering).

O experimento foi configurado inicialmente com:

K = 2
Dois grupos de mensagens.
Utilização dos embeddings como entrada do algoritmo.

O objetivo é verificar se o algoritmo consegue encontrar grupos de mensagens com características semelhantes sem receber previamente a informação de quais mensagens são golpes.

              EMBEDDINGS
                   │
                   ↓
                K-MEANS
                 K = 2
                   │
           ┌───────┴───────┐
           ↓               ↓
        GRUPO 0         GRUPO 1
           │               │
           ↓               ↓
      Mensagens         Mensagens
     semelhantes       semelhantes

### 4. Avaliação do agrupamento

Como o K-Means não recebe os rótulos durante o treinamento, a avaliação utiliza métricas próprias de agrupamento.

Foi utilizado o Silhouette Score, que permite avaliar o quanto os elementos estão bem posicionados dentro de seus respectivos grupos e o quanto os grupos estão separados entre si.

De forma geral:

Silhouette Score	Interpretação
Próximo de 1	Grupos bem separados
Próximo de 0	Grupos pouco separados
Abaixo de 0	Possível agrupamento inadequado

### 5. Visualização dos grupos

Como os embeddings possuem várias dimensões, será utilizada uma técnica de redução de dimensionalidade para possibilitar a visualização dos grupos.

Foi utilizado o PCA (Principal Component Analysis) para reduzir a representação dos embeddings para duas dimensões.

Embeddings
    │
    ↓
   PCA
    │
    ↓
2 dimensões
    │
    ↓
Gráfico dos grupos

A visualização permite observar se os grupos encontrados pelo K-Means apresentam uma separação visual significativa.

### 6. Análise dos grupos

Após o agrupamento, os grupos serão analisados para identificar suas principais características.

Serão observados:

Quantidade de mensagens em cada grupo.
Mensagens representativas de cada grupo.
Características predominantes.
Padrões textuais encontrados.
Distribuição da variável Possivel golpe dentro de cada grupo.

A variável Possivel golpe será utilizada somente nesta etapa de análise, após o treinamento, para verificar a relação entre os grupos encontrados e os rótulos existentes no dataset.

### 7. Comparação com o target

Embora o Possivel golpe não seja utilizado para treinar o K-Means, seus valores poderão ser comparados posteriormente com os grupos encontrados.

Essa análise permitirá verificar, por exemplo, se determinado grupo possui uma concentração maior de mensagens originalmente classificadas como possíveis golpes.

              K-MEANS
                 │
                 ↓
          Grupos encontrados
                 │
                 ↓
       Análise dos grupos
                 │
                 ↓
       Comparação com target
                 │
                 ↓
         Possível relação

Essa comparação não significa que o K-Means realizou uma classificação supervisionada. O algoritmo apenas identificou grupos com base nas características das mensagens.

### 8. Resultado do experimento

O resultado do agrupamento será analisado considerando o Silhouette Score, a distribuição das mensagens entre os grupos e a relação observada entre os agrupamentos e a variável Possivel golpe.

Silhouette Score: A preencher após o experimento

Resultado da análise: A preencher após a execução do modelo

O objetivo dessa etapa não é substituir o modelo supervisionado, mas verificar se existem estruturas ou padrões naturais nas mensagens que possam contribuir para a compreensão do dataset e do problema.

### 9. Conclusão do experimento

O aprendizado não supervisionado será utilizado como uma abordagem complementar ao aprendizado supervisionado.

Enquanto o modelo supervisionado busca responder:

"A mensagem pode ser classificada como um possível golpe?"

o aprendizado não supervisionado busca responder:

"Existem grupos ou padrões naturais entre as mensagens?"

Dessa forma, as duas abordagens possuem objetivos diferentes e complementares dentro do projeto.

Fluxograma
                    DATASET PRONTO
                          │
                          ↓
                 SELEÇÃO DAS MENSAGENS
                          │
                          ↓
                   NORMALIZAÇÃO
                          │
                          ↓
                    EMBEDDINGS
                          │
                          ↓
                   VETORES NUMÉRICOS
                          │
                          ↓
                       K-MEANS
                        K = 2
                          │
                ┌─────────┴─────────┐
                ↓                   ↓
             GRUPO 0             GRUPO 1
                │                   │
                └─────────┬─────────┘
                          ↓
                   SILHOUETTE SCORE
                          │
                          ↓
                         PCA
                          │
                          ↓
                 VISUALIZAÇÃO DOS
                     GRUPOS
                          │
                          ↓
                  ANÁLISE DOS GRUPOS
                          │
                          ↓
              COMPARAÇÃO COM TARGET
                          │
                          ↓
               ANÁLISE DOS PADRÕES
                          │
                          ↓
                     CONCLUSÃO
Relação entre os dois tipos de aprendizado
                 MACHINE LEARNING
                        │
           ┌────────────┴────────────┐
           ↓                         ↓
    SUPERVISIONADO            NÃO SUPERVISIONADO
           │                         │
           ↓                         ↓
       XGBoost                    K-Means
           │                         │
           ↓                         ↓
     TF-IDF + 24                Embeddings
      Features                       │
           │                         │
           ↓                         ↓
   Classificar SMS             Agrupar SMS
           │                         │
           ↓                         ↓
  Golpe / Não golpe          Grupo 0 / Grupo 1
           │                         │
           ↓                         ↓
     Predição                 Descoberta de
                               padrões
=======
