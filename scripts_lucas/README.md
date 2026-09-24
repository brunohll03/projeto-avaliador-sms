# Classificador de SMS — versão com regras locais

Este pacote executa as 24 features usando somente a biblioteca padrão do
**Python 3.9 ou superior**. Não precisa de `pip install`, Java, modelos ou internet.

Compacte e envie esta pasta inteira. Após extrair, mantenha a subpasta
`classificador_features_sms` com esse nome: ela é o pacote usado pelos imports.
Os datasets não são necessários para executar uma mensagem e não estão incluídos.
Para processar um dataset real, envie também o CSV desejado.

## Uma mensagem por vez

Abra o terminal nesta pasta (`entrega_sem_bibliotecas`) e execute:

```bash
python3 -m classificador_features_sms.main
```

Digite o SMS quando aparecer `Digite o SMS:` e pressione Enter. Para informar
diretamente o texto ou consultar detalhes:

```bash
python3 -m classificador_features_sms.main 'Informe sua senha agora.'
python3 -m classificador_features_sms.main --detalhes 'Informe seu CPF.'
```

No Windows, se o comando `python3` não existir, use `py -3` ou `python`.

## Preencher um CSV

Coloque seu CSV nesta pasta. Ele deve estar em UTF-8 e conter a coluna `Mensagem`.
Aceita separação por vírgula, ponto e vírgula ou tabulação.

```bash
python3 -m classificador_features_sms.classificar_csv 'entrada.csv' --saida 'classificado.csv'
```

As 24 features são preenchidas com `0` ou `1`. Cabeçalhos ausentes são adicionados;
valores existentes de features são recalculados. `Mensagem`, `possivel_golpe` e
outras colunas são preservadas. Sem `--saida`, o próprio CSV é atualizado.
A saída só é substituída quando todas as mensagens terminarem sem erro.

Este pacote usa sempre as regras de `features/`; não é preciso escolher um método.

## Comparar com uma referência anotada

```bash
python3 -m classificador_features_sms.comparar_csv 'referencia.csv' 'classificado.csv' --saida 'comparacao'
```

Gera `resumo.json`, `metricas.csv` e `divergencias.csv`. A comparação alinha pelo
texto exato de `Mensagem`, mesmo se a ordem das linhas mudar. Mensagens duplicadas
ou vazias são rejeitadas por não permitirem alinhamento inequívoco.

O relatório mostra acurácia, precisão, revocação, F1 e cobertura por feature.
Colunas com categorias não binárias são excluídas: por exemplo, `carga_emocional`
com `Baixo/Médio/Alto` não é comparada automaticamente com `0/1`. Campos vazios
não contam como acertos. Confira cobertura e divergências junto com as métricas.

## Executar os testes

Ainda nesta pasta:

```bash
python3 -m unittest discover -s classificador_features_sms/tests -t . -v
```

## Conteúdo

- `main.py`: execução de uma mensagem.
- `classificador.py`: reúne as 24 features.
- `features/`: uma implementação por feature.
- `regras.py` e `urls.py`: funções compartilhadas.
- `classificar_csv.py`: processamento de todas as mensagens de um CSV.
- `comparar_csv.py`: comparação com uma referência.
- `tests/`: testes automatizados.

Os arquivos acima ficam dentro de `classificador_features_sms/`.
Também é possível entrar nessa subpasta e executar `python3 main.py`,
`python3 classificar_csv.py ...` ou `python3 comparar_csv.py ...` diretamente.

## Significado dos resultados

`1` significa que a feature foi detectada pelas regras; `0`, que não foi detectada.
As regras são aproximações e podem falhar. O programa extrai características,
mas não decide se a mensagem é golpe e não calcula o rótulo `possivel_golpe`.
Nesta versão, `carga_emocional` também é binária.
