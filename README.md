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
projeto/
│
├── data/
│   └── dataset.csv
│
├── models/
│   └── modelos.py
│
├── src/
│   ├── preprocessing/
│   │   └── limpeza.py
│   │
│   ├── supervised/
│   │   └── classificacao.py
│   │
│   ├── unsupervised/
│   │   └── clustering.py
│   │
│   ├── evaluation/
│   │   └── metricas.py
│   │
│   └── visualization/
│       └── graficos.py
│
├── backend/
│   └── app.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
│
└── README.md
