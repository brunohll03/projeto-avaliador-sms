# Projeto – Avaliação de Informações por IA

Sistema desenvolvido em Python para auxiliar usuários na avaliação de mensagens SMS, utilizando técnicas de Machine Learning sem substituir o pensamento crítico.

## Objetivo

Analisar mensagens SMS e apresentar classificações que auxiliem o usuário a identificar diferentes características da informação.

## Classificações

- Linguagem emocional: baixa, média ou alta
- Fato ou opinião: fato verificável, opinião ou interpretação
- Intenção: informativa, persuasão ou promocional
- Spam: sim ou não
- Categoria: social, atualização ou compras

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
projeto_sms_golpes/
+-- README.md
+-- requirements.txt
+-- .gitignore
+-- app/
¦   +-- app.py
+-- data/
¦   +-- raw/
¦   +-- processed/
+-- models/
+-- notebooks/
+-- reports/
+-- src/
```

## Como executar

1. Crie um ambiente virtual com Python 3.11+.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rode a aplicação:
   ```bash
   python app/app.py
   ```

## Observações

Este projeto trabalha com modelos de classificação de SMS com foco em análise de risco, linguagem emocional e mensagens potencialmente fraudulentas.
