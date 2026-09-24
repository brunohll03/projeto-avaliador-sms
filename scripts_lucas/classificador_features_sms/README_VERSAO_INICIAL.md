# Classificador de features de SMS

Primeira versão baseada nas 24 definições do **Dicionário de Features.docx** fornecido para o projeto de residência. Recebe um SMS em português e retorna um dicionário com os nomes originais das features e valores inteiros: **0 = não detectada pelas regras**, **1 = detectada**. Não produz uma classificação final de golpe ou mensagem legítima.

Usa apenas a biblioteca padrão do **Python 3.9 ou superior**, sem instalação de pacotes, modelos, acesso à internet ou leitura de datasets. Os comentários antes dos imports explicam as bibliotecas utilizadas; os métodos de carga emocional e erros de escrita têm blocos próprios de explicação. O Word foi usado como referência de desenvolvimento e não precisa estar presente para executar os scripts.

## Executar

A partir da raiz do projeto:

```bash
python3 -m classificador_features_sms.main 'Informe seu CPF e clique em https://bit.ly/exemplo para confirmar.'
```

Também funciona com o caminho do arquivo:

```bash
python3 classificador_features_sms/main.py 'Nunca compartilhe sua senha.'
```

Sem argumentos, o terminal solicita a mensagem. Para receber um texto pela entrada padrão:

```bash
python3 -m classificador_features_sms.main - < mensagem.txt
```

Cada execução analisa **uma mensagem completa**; várias linhas recebidas pela entrada padrão compõem um único SMS. A saída é JSON contendo sempre as 24 features. A string vazia retorna todas como zero; a API rejeita valores que não sejam strings.

Para incluir medidas complementares:

```bash
python3 -m classificador_features_sms.main --detalhes 'Alerta! Informe seu CPF em https://exemplo.com.'
```

Nesse modo, a saída contém `versao_regras`, `features` (as mesmas 24 classificações) e `detalhes`: quantidade de URLs, contagens e proporção emocional, quantidade de erros, taxa de erros por palavra e sugestões de correção. O texto recebido não é alterado nem salvo em arquivo pelo classificador.

## Preencher as features de um CSV

Estes comandos partem de dentro da pasta `classificador_features_sms`.
O script recebe um CSV UTF-8 com a coluna `Mensagem`, classifica cada registro
e preenche as 24 features. Preserva as mensagens, a ordem dos registros,
`possivel_golpe` e outras colunas. Features já preenchidas são recalculadas;
cabeçalhos de features ausentes são acrescentados. Aceita separação por vírgula,
ponto e vírgula ou tabulação.

Para usar as regras de `features/` e atualizar o próprio CSV:

```bash
python3 classificar_csv.py 'DATASET - Dataset_limpo_sem_atributos copy.csv' --metodo regras
```

Para usar `features_bibliotecas/`, após instalar suas dependências conforme
o [guia dessa versão](features_bibliotecas/README.md):

```bash
source features_bibliotecas/.venv/bin/activate
python classificar_csv.py 'DATASET - Dataset_limpo_sem_atributos copy.csv' --metodo bibliotecas
```

A versão com bibliotecas mantém uma única instância do modelo e do corretor
para todas as mensagens. A primeira execução pode baixar esses recursos.
Aceita também `--limiar 0.70` e `--somente-local`, com o mesmo significado da
interface de uma mensagem. O LanguageTool também precisa estar em cache para
uma execução totalmente sem rede.

Para salvar em outro arquivo, acrescente `--saida`:

```bash
python3 classificar_csv.py 'DATASET - Dataset_limpo_sem_atributos copy.csv' --metodo regras --saida 'dataset_classificado_regras.csv'
```

O progresso aparece no terminal. A saída só é substituída após todas as mensagens
serem classificadas; erros ou interrupção mantêm o arquivo anterior. Corrija o
problema e execute novamente desde o início. O script não calcula `possivel_golpe`.

## Comparar a classificação com o dataset de referência

Dentro de `classificador_features_sms`, execute com o CSV de referência primeiro
e o CSV classificado depois. Não é necessário instalar bibliotecas:

```bash
python3 comparar_csv.py 'dataset_estaticos/DATASET - Dataset_limpo_V1.csv' 'DATASET - Dataset_limpo_sem_atributos copy.csv' --saida comparacoes/copy
python3 comparar_csv.py 'dataset_estaticos/DATASET - Dataset_limpo_V1.csv' 'DATASET - Dataset_limpo_sem_atributos copy 2.csv' --saida comparacoes/copy_2
```

O script alinha pelo texto exato da coluna `Mensagem`, mesmo com linhas fora de
ordem. Rejeita mensagens repetidas ou vazias para evitar alinhamento ambíguo.
Não altera os CSVs de entrada. A pasta escolhida recebe três relatórios;
uma nova execução na mesma pasta substitui os relatórios anteriores:

- `resumo.json`: concordância global, cobertura, mensagens ausentes/extras e rótulos alterados.
- `metricas.csv`: métricas por feature, valores encontrados e motivos de exclusão.
- `divergencias.csv`: mensagem, números dos registros (contados a partir de 1, sem cabeçalho),
  feature, valor de referência, valor obtido e motivo da divergência. Inclui
  campos vazios, mensagens sem par e alterações em `possivel_golpe`.

As métricas usam a classe `1` como positiva:

- **Acurácia:** proporção de valores iguais à referência.
- **Precisão:** entre os valores previstos como `1`, quantos eram `1` na referência.
- **Revocação:** entre os valores `1` da referência, quantos foram detectados.
- **F1:** combina precisão e revocação; ajuda a avaliar features em que predominam zeros.
- **VP/VN/FP/FN:** verdadeiros positivos, verdadeiros negativos, falsos positivos e falsos negativos.
- **Cobertura:** proporção dos dados que pôde ser avaliada. Células vazias não viram zero.

Métricas sem denominador aparecem como `n/a` no terminal, `null` no JSON e vazias
no CSV. A acurácia global soma os acertos e divide pelas células binárias válidas;
a taxa de mensagens idênticas considera apenas mensagens completas nas features
compatíveis. Confira a cobertura e as exclusões junto com esses resultados.

Na referência atual, `carga_emocional` contém `Baixo`, `Médio` e `Alto`, mas os
classificadores produzem `0` e `1`. Essa coluna fica fora das métricas binárias,
com o motivo `valores_nao_binarios`. Qualquer coluna com valores não binários é
excluída por inteiro; não há conversão automática entre escalas. `Coluna 27` e
colunas que não são features não entram na avaliação. `possivel_golpe` é conferido
somente para verificar se seus rótulos foram preservados, pois não é uma predição
destes scripts.

A avaliação mede concordância com as anotações fornecidas. Ela só representa
acertos do classificador na medida em que essa referência esteja correta.

## Usar em outro código Python

Execute o código abaixo a partir da raiz, ou disponibilize a raiz no caminho de importação do Python:

```python
from classificador_features_sms import classificar_sms

features = classificar_sms("Informe sua senha de acesso.")
print(features)                    # Dicionário com todas as 24 features.
print(features["solicita_senha"])  # 1
```

Cada feature também pode ser chamada isoladamente, com a mesma interface:

```python
from classificador_features_sms.features.solicita_senha import classificar

print(classificar("Digite sua senha."))        # 1
print(classificar("Nunca envie sua senha."))   # 0
print(classificar("Sua senha foi alterada."))  # 0
```

Os arquivos de `features/` são módulos importáveis; o arquivo executável que recebe o SMS é `main.py`.

## Organização

```text
classificador_features_sms/
├── main.py            # Interface de terminal e saída JSON.
├── classificador.py   # Executa as 24 funções e reúne as classificações.
├── regras.py          # Normalização, ações, negação e associação de termos.
├── urls.py            # Extração e validação estrutural de URLs.
├── features/          # Um arquivo .py para cada feature da tabela abaixo.
└── tests/             # Exemplos do dicionário e contraexemplos.
```

## Regras da versão 1.0.0

Cada nome abaixo corresponde a `features/<nome>.py`. As regras semânticas são aproximações determinísticas das definições do documento, adequadas como ponto de partida para revisão.

| Feature | Critério implementado |
| --- | --- |
| `solicita_senha` | Verbo de solicitação associado a senha; exclui avisos negativos locais. |
| `solicita_codigo_autenticacao` | Solicitação de token, OTP ou código com contexto de autenticação/SMS/WhatsApp. Código de segurança associado a cartão é tratado como cartão. |
| `solicita_dados_bancarios` | Pedido de banco, agência, número ou dados de conta bancária. A palavra conta isolada não basta. |
| `solicita_dados_pessoais` | Solicitação de CPF, RG, nome completo, nascimento, endereço, telefone, e-mail ou dados pessoais/cadastrais. |
| `solicita_dados_cartao` | Pedido de número/dados/validade de cartão, CVV/CVC ou código de segurança com contexto de cartão. |
| `solicita_atualizacao_cadastro` | Atualizar, confirmar, regularizar, completar ou validar cadastro/dados; inclui finalidade explícita de um comando de acesso. |
| `solicita_pagamento` | Pedido para pagar, quitar, depositar ou movimentar valor, incluindo PIX. |
| `solicita_clique` | Clicar, acessar, tocar ou abrir associado a link, botão, endereço, URL ou indicação como aqui. |
| `solicita_ligacao` | Pedido de ligação ou contato por telefone. Um rótulo como Telefone: não é pedido. |
| `menciona_bloqueio_conta` | Bloqueio, suspensão ou cancelamento próximo de conta, cartão, cadastro, acesso ou serviço. |
| `carga_emocional` | Pelo menos uma palavra do léxico emocional local; a proporção original fica disponível em `medir` e `--detalhes`. |
| `possui_urgencia` | Pressão temporal explícita ou uma ação associada a agora, hoje, imediatamente ou prazo curto. |
| `possui_ameaca` | Consequência negativa associada a condição de omissão, alternativa negativa ou comando para evitar a consequência. |
| `possui_linguagem_alarmista` | Expressões como alerta, atenção, perigo, situação grave e atividade suspeita. |
| `possui_recompensa` | Afirmação de ganho/seleção ou prêmio, recompensa, brinde, bônus ou presente oferecido. |
| `possui_reembolso` | Reembolso/restituição disponível, direito a recebimento ou afirmação de valor a receber. |
| `possui_vantagem_inesperada` | Recompensa/seleção ou indícios de benefício extraordinário, dinheiro liberado e oportunidade exclusiva. |
| `possui_oferta_financeira` | Crédito pré-aprovado/liberado ou proposta explícita de empréstimo, financiamento, investimento ou ganho. |
| `possui_url` | URL estruturalmente reconhecível, com validação do domínio ou IP. |
| `possui_url_encurtada` | Host da URL na lista fixa: bit.ly, tinyurl.com, t.co, is.gd e ow.ly. |
| `possui_telefone` | Número brasileiro com DDD válido e prefixo de fixo/celular, ou 0800/0300/0303/0900. |
| `possui_pix` | Palavra PIX completa, ignorando caixa e sem exigir pedido de pagamento. |
| `possui_erros_ortografia_gramatica` | Pelo menos um erro de uma lista manual de grafias e padrões gramaticais. |
| `possui_chamada_acao` | Verbo imperativo afirmativo ou algumas construções de pedido indireto. |

## Escolhas e limites desta primeira versão

- **Contexto dos pedidos:** normaliza acentos/caixa, separa frases e busca até oito palavras entre verbo e dado solicitado, interrompendo a busca antes de outra ação. Negações próximas como nunca compartilhe e não informe são excluídas. Não há análise sintática completa: citações, discurso relatado, condições complexas, pedidos com termos distantes e construções ausentes do vocabulário podem ser classificados incorretamente.
- **Carga emocional binária:** o documento propõe uma proporção. Para atender à saída inicial 0/1, adotamos `1` quando há pelo menos uma ocorrência do léxico local, equivalente a proporção maior que zero. Mantemos também `ocorrências emocionais / total de palavras analisáveis`, sem faixas de intensidade. O léxico manual inclui indícios de alarme e perda, não é LIWC nem um instrumento linguístico validado. Negar uma emoção não remove sua ocorrência lexical.
- **Erros de escrita:** só detecta as grafias e construções cadastradas no módulo. Não avalia toda a ortografia ou gramática do português. Abreviações, gírias, emojis, palavras desconhecidas, falta de acentos e falta de pontuação não geram erro automaticamente. Cada padrão gramatical conta como uma ocorrência, mesmo se abranger várias palavras; a taxa auxiliar usa o total de palavras do SMS sem URLs.
- **Urgência:** prazos numéricos reconhecidos vão de 1 a 60 minutos ou de 1 a 24 horas, além das expressões temporais listadas no código. Esses limites são uma escolha operacional inicial, não limites fornecidos pelo dicionário. Não interpreta datas de calendário, prazos por extenso ou a data atual. Uma entrega ocorrida hoje não deve ser marcada só pela data.
- **URLs:** aceita HTTP, HTTPS, www e, como extensão inicial, domínios sem esquema de uma lista de sufixos frequentes. Para URLs com esquema, a validação não depende dessa lista. Não verifica existência, reputação ou destino de redirecionamento. Não reconhece todas as ofuscações, como `hxxp` e `[.]`. A lista de encurtadores é fixa e não afirma que os serviços estejam ativos.
- **Telefones:** exige DDD para números comuns; não detecta números locais isolados. Mascara CPF/CNPJ formatados, CEP, datas, valores, URLs e números rotulados como código/protocolo etc. Um CPF sem pontuação e sem rótulo pode ser estruturalmente indistinguível de um celular; nenhum método apenas estrutural garante resolver essa ambiguidade. Não confirma que uma linha exista.
- **Vantagem inesperada:** não é possível saber pelo SMS o que a pessoa realmente esperava. A regra usa indícios textuais explícitos, com sobreposição intencional com recompensa. Reembolso e oferta financeira não ativam automaticamente essa feature.
- **Significado da saída:** presença de uma feature não prova golpe; ausência não prova que a característica esteja semanticamente ausente. A versão ainda precisa de avaliação em SMS reais anotados, principalmente para as features subjetivas.

## Validar e ajustar

```bash
python3 -m unittest discover -s classificador_features_sms/tests -v
```

Os testes cobrem os 24 exemplos principais do documento, 98 contraexemplos, formatos adicionais de telefones/URLs/pedidos, ajustes de contexto, contrato de saída e cálculos auxiliares. São testes de comportamento, não uma medição de precisão em um dataset.

Para ajustar uma feature, edite seu módulo e acrescente um exemplo positivo e um contraexemplo aos testes. Altere `regras.py` com cuidado porque suas funções são compartilhadas. Ao mudar regras ou vocabulários após começar a classificar um dataset, incremente `VERSAO_REGRAS` em `classificador.py` e reexecute a classificação para não misturar metodologias.
