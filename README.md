# Projeto – Avaliação de Informações por IA

Sistema desenvolvido em Python para auxiliar usuários na avaliação de mensagens SMS, utilizando técnicas de Machine Learning sem substituir o pensamento crítico.

## Objetivo

Analisar mensagens SMS e apresentar classificações que auxiliem o usuário a identificar diferentes características da informação.

## Classificações

- **Linguagem emocional:** baixa, média ou alta
- **Fato ou opinião:** fato verificável, opinião ou interpretação
- **Intenção:** informativa, persuasão ou promocional
- **Spam:** sim ou não
- **Categoria:** social, atualização ou compras

## Tecnologias

- Python
- Machine Learning
- Aprendizado supervisionado
- Aprendizado não supervisionado
- Pandas
- Scikit-learn
- Visualização de dados

## Estrutura do Projeto

```text
projeto-avaliador-sms/
│
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
│
├── dataset/
│   ├── original/
│   │   └── dataset_original.csv
│   │
│   └── processed/
│       └── dataset_final.csv
│
├── notebooks/
│   ├── 01_analise_dataset.ipynb
│   ├── 02_aprendizado_supervisionado.ipynb
│   ├── 03_aprendizado_nao_supervisionado.ipynb
│   ├── 04_avaliacao_modelos.ipynb
│   └── 05_visualizacoes.ipynb
│
├── src/
│   │
│   ├── data/
│   │   ├── load_data.py
│   │   └── clean_data.py
│   │
│   ├── models/
│   │   ├── supervised.py
│   │   ├── unsupervised.py
│   │   └── predict.py
│   │
│   ├── evaluation/
│   │   └── metrics.py
│   │
│   └── visualization/
│       └── plots.py
│
├── models/
│   ├── classification_model.pkl
│   └── clustering_model.pkl
│
├── backend/
│
└── frontend/
   
```


## Abordagens de Machine Learning

### Aprendizado Supervisionado

Utilização de algoritmos de classificação para identificar as categorias das mensagens a partir de dados previamente rotulados.

### Aprendizado Não Supervisionado

Utilização de técnicas de **clustering** para identificar grupos e padrões naturais entre as mensagens.

## Avaliação

Serão utilizadas métricas para avaliar o desempenho dos modelos:

- Accuracy
- Precision
- Recall
- F1-Score
- Matriz de Confusão

Também serão analisados os erros dos modelos, principalmente nas classificações relacionadas a spam.

## Visualização

Serão implementadas visualizações para auxiliar na análise dos dados e dos modelos:

- Distribuição das categorias;
- Matriz de confusão;
- Visualização dos agrupamentos encontrados pelo clustering;
- Distribuição das classificações;
- Comparação de desempenho entre modelos.

## Aspectos Éticos

O projeto considera os seguintes aspectos:

- Privacidade dos usuários;
- Anonimização das mensagens;
- Consentimento para utilização dos dados;
- Possíveis vieses do dataset;
- Transparência sobre as limitações dos modelos;
- Risco de confiança excessiva na classificação da IA.

## Princípio da Solução

A ferramenta tem como objetivo **auxiliar o usuário na avaliação das informações**, fornecendo indicadores e classificações que apoiem o pensamento crítico.

A IA não deve substituir a análise do usuário nem determinar, de forma definitiva, se uma mensagem é verdadeira ou falsa.
