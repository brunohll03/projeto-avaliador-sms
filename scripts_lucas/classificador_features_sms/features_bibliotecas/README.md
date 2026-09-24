# Features de SMS com bibliotecas especializadas

**Versão experimental: requer validação em SMS anotados antes de uso operacional.**

Esta pasta é uma cópia de `features/` com os **24 módulos reescritos**. Cada arquivo conserva `classificar(sms: str) -> int`. Há um novo classificador e uma interface de terminal dentro desta pasta. A execução original de `classificador_features_sms.main` continua usando a implementação anterior.

Uma **feature** é uma característica mensurável da mensagem. A saída é um vetor de 24 inteiros: **1 = detectada pelo método; 0 = não detectada**. As características podem coexistir e não constituem uma classificação final de golpe. Por exemplo, um SMS legítimo também pode conter URL, PIX ou urgência.

## Como os novos métodos funcionam

| Método | Aplicação | O que a biblioteca faz |
| --- | --- | --- |
| Transformers + PyTorch, modelo NLI multilíngue | 19 features semânticas, incluindo emoção | Compara o SMS com uma hipótese escrita em português e calcula um escore independente por característica. |
| linkify-it-py | URL e URL encurtada | Extrai links e seus limites. Validamos o host real; a identificação de encurtadores usa uma lista explícita. |
| phonenumbers | Telefone | Reconhece números com metadados da libphonenumber; BR é a região padrão e números internacionais com + também são aceitos. |
| regex | PIX e máscaras auxiliares | Faz correspondência literal com limites Unicode. PIX é uma característica lexical, portanto não exige rede neural. |
| language-tool-python + LanguageTool local | Ortografia e gramática | Consulta o dicionário e as regras de pt-BR. Retorna posição, regra e sugestões dos apontamentos de ortografia/gramática. |

O modelo escolhido é `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`. Ele é um classificador geral de inferência linguística, **não um modelo treinado especificamente nestas 19 features de SMS**. O uso em português aproveita transferência multilíngue; português não está entre os idiomas de avaliação XNLI apresentados no cartão. Não há dados anotados suficientes nesta pasta para afirmar sua qualidade neste domínio.

**Zero-shot** significa usar descrições das classes sem treinar um classificador novo com exemplos dessas classes. A mensagem funciona como premissa, e uma frase como “O remetente pede que o destinatário informe sua senha” funciona como hipótese. O modelo estima se há apoio ou contradição. Cada par SMS/hipótese é avaliado separadamente, permitindo várias características positivas simultaneamente. Não se usa um modelo gerador nem se pede que ele execute instruções contidas no SMS.

O escore é o softmax de apoio considerando **apoio, neutralidade e contradição** no denominador. Usamos a pipeline `text-classification` com pares SMS/hipótese e `top_k=None` para preservar as três saídas do modelo NLI. Isso continua sendo classificação zero-shot; evitamos descartar a classe neutra como ocorre na pipeline zero-shot pronta em modo multilabel. A decisão inicial é `escore >= 0.70`. **Esse limiar é uma escolha inicial não calibrada**, e o escore não representa probabilidade de golpe nem confiança estatisticamente validada. Citações, negação, ironia e pedidos indiretos podem causar erros. A redação das hipóteses também influencia os resultados.

## Instalar e executar

Requer **Python 3.10+** e **Java 17+** para LanguageTool. Os comandos abaixo partem da pasta `Residência Tecnológica - IA`:

```bash
python3 -m venv classificador_features_sms/features_bibliotecas/.venv
source classificador_features_sms/features_bibliotecas/.venv/bin/activate
python -m pip install -r classificador_features_sms/features_bibliotecas/requirements.txt
java -version
python -m classificador_features_sms.features_bibliotecas.main --detalhes 'Informe sua senha agora em https://bit.ly/exemplo.'
```

A primeira classificação semântica baixa os pesos do modelo; o primeiro uso do corretor baixa o servidor LanguageTool 6.8. Reserve espaço e tempo para esses downloads, da ordem de centenas de MB para os pesos e o arquivo do servidor; os caches descompactados e as dependências exigem espaço adicional. Após o download, a inferência é local em CPU por padrão e o corretor roda em um servidor Java local; o SMS não é enviado a uma API de classificação. A importação dos módulos e a mensagem vazia não carregam esses modelos.

Os caches padrão ficam nas pastas usadas pelas bibliotecas. Para mantê-los junto da nova versão, defina antes de executar:

```bash
export HF_HOME="$PWD/classificador_features_sms/features_bibliotecas/.cache/huggingface"
export LTP_PATH="$PWD/classificador_features_sms/features_bibliotecas/.cache/languagetool"
```

`--somente-local` impede download **do modelo NLI**; para executar todo o sistema sem rede, o LanguageTool também deve estar previamente disponível no cache. O programa não troca para uma API pública quando há falha. Problema de instalação, download ou Java produz erro em vez de uma classificação fictícia.

```bash
# JSON somente com os 24 valores:
python -m classificador_features_sms.features_bibliotecas.main 'Recebemos seu PIX.'

# Toda a entrada padrão forma uma única mensagem:
python -m classificador_features_sms.features_bibliotecas.main --detalhes - < mensagem.txt

# Também funciona pelo caminho do arquivo:
python classificador_features_sms/features_bibliotecas/main.py --help
```

## Usar no Python

```python
from classificador_features_sms.features_bibliotecas import classificar_sms, analisar_sms

features = classificar_sms('Informe seu CPF e clique em https://exemplo.com.')
detalhes = analisar_sms('Sua conta foi bloquiada.')
print(features)
print(detalhes['detalhes']['erros_detectados'])
```

Para apenas uma feature:

```python
from classificador_features_sms.features_bibliotecas.solicita_senha import classificar, medir
from classificador_features_sms.features_bibliotecas.possui_telefone import extrair_telefones

print(classificar('Informe sua senha.'))
print(medir('Nunca compartilhe sua senha.'))  # Escore, hipótese, limiar e valor.
print(extrair_telefones('Telefone: (19) 99999-1234.'))
```

Para reutilizar o modelo e encerrar explicitamente o processo Java:

```python
from classificador_features_sms.features_bibliotecas import ClassificadorFeatures, Configuracao

config = Configuracao(
    limiar=0.70,
    limiares={'solicita_senha': 0.80},  # Exemplo de configuração; não é calibração.
    dispositivo='cpu',
)
with ClassificadorFeatures(config) as classificador:
    resultado = classificador.analisar_sms('Informe sua senha.')
    print(resultado['features'])
```

Os escores semânticos e hipóteses ficam em `detalhes.semanticas`. URLs, telefones e erros fornecem evidências estruturais. O escore NLI por si só não identifica qual trecho causou a decisão. `configuracao.revisao_carregada` registra o commit do modelo; passe esse valor em `Configuracao(revisao=...)` ou `--revisao` para repetir a escolha dos pesos. Fixe também versões de dependências e limiares em experimentos comparativos.

Mensagens que excedam o limite do modelo com as hipóteses são rejeitadas para evitar truncamento silencioso. A API rejeita `None`, números e listas. Mensagens vazias retornam 24 zeros.

## Mudanças de significado em relação à cópia original

- **Carga emocional:** antes era presença e proporção de palavras de um léxico manual; agora é um escore NLI da mensagem. `medir()` retorna escore, hipótese, limiar e valor. Não há campo `proporcao` porque ele seria enganoso. URLs são mascaradas nessa análise.
- **Ortografia/gramática:** passa a usar um corretor amplo. Falta de acento, abreviações e nomes próprios podem gerar apontamentos, diferentemente da lista restrita anterior. Só contam tipos `misspelling` e `grammar`; estilo e tipografia ficam de fora. Não calculamos a antiga taxa por palavra.
- **Telefone:** metadados de validade substituem a lista de DDD/prefixos; inclui internacionais explícitos. Alguns números aceitos pelas regras antigas podem ser rejeitados e vice-versa. Não confirma linha ativa. CPF sem rótulo pode continuar indistinguível de celular.
- **URLs:** a cobertura de domínios passa a depender de linkify-it-py. Encurtadores continuam exigindo uma lista conhecida; não existe identificação universal apenas pelo tamanho do link.
- **PIX:** continua literal, inclusive em uma frase negativa, mas não conta quando está apenas dentro de uma URL.
- **Features semânticas:** os nomes foram preservados, mas os resultados podem divergir das regras anteriores. Não misture as duas versões em um mesmo dataset sem identificar o método.

A nova versão é identificada por `2.0.0-bibliotecas`. Os scripts independem dos módulos `regras.py`, `urls.py` e `features/` antigos.

## Explicação das 24 features

Cada módulo inclui comentários sobre o método, a definição, exemplos e limites. Para as 19 features abaixo, 1 significa escore NLI igual ou superior ao limiar configurado; os exemplos positivos e negativos indicam a interpretação desejada, não resultados garantidos do modelo.

### `solicita_senha`

Detecta pedido de senha; menção a senha alterada e conselho para nunca compartilhar são controles negativos.

**Hipótese avaliada:** O remetente pede que o destinatário informe, envie ou digite sua senha.

- Positivo esperado: Para confirmar seu cadastro, informe sua senha de acesso no formulário abaixo.
- Negativo esperado: Nunca compartilhe sua senha.

### `solicita_codigo_autenticacao`

Distingue autenticação de cupom, código de produto e CVV de cartão; informar um código ao usuário não é solicitar esse código.

**Hipótese avaliada:** O remetente pede que o destinatário forneça um código de autenticação, token ou código recebido por SMS ou WhatsApp.

- Positivo esperado: Digite aqui o código de 6 números que você recebeu por SMS para confirmar sua conta.
- Negativo esperado: Um código será enviado por SMS.

### `solicita_dados_bancarios`

Não confundir conta de e-mail nem simples aviso de depósito com pedido de dados bancários.

**Hipótese avaliada:** O remetente solicita dados bancários do destinatário, como banco, agência ou número de conta bancária.

- Positivo esperado: Para liberar seu benefício, informe o número do banco, agência e conta.
- Negativo esperado: Sua conta está ativa.

### `solicita_dados_pessoais`

Exige intenção de solicitar; um aviso de CPF atualizado não basta.

**Hipótese avaliada:** O remetente pede que o destinatário forneça dados pessoais, como CPF, RG, nome completo, endereço ou data de nascimento.

- Positivo esperado: Para atualizar seu cadastro, informe seu CPF, nome completo e data de nascimento.
- Negativo esperado: Seu CPF foi atualizado.

### `solicita_dados_cartao`

Dados de cartão são distintos de agência e conta bancária; pode coexistir com pedido de dados pessoais.

**Hipótese avaliada:** O remetente solicita o número, a validade, o CVV ou outros dados do cartão do destinatário.

- Positivo esperado: Para receber o reembolso, informe o número do cartão, validade e código de segurança.
- Negativo esperado: Seu cartão chegou.

### `solicita_atualizacao_cadastro`

Inclui finalidade de um comando de acesso. Informar que o cadastro está desatualizado não é necessariamente um pedido.

**Hipótese avaliada:** O remetente pede que o destinatário atualize, confirme ou regularize seu cadastro ou seus dados cadastrais.

- Positivo esperado: Seu cadastro está desatualizado. Acesse o link abaixo para confirmar seus dados.
- Negativo esperado: Cadastro atualizado.

### `solicita_pagamento`

PIX recebido é comprovante; não deve ser confundido com pedido para pagar.

**Hipótese avaliada:** O remetente pede que o destinatário faça um pagamento, depósito ou transferência de dinheiro.

- Positivo esperado: Para evitar o cancelamento do pedido, faça o pagamento de R$ 29,90 ainda hoje.
- Negativo esperado: O pagamento foi recebido.

### `solicita_clique`

Ter URL não basta. Conselho para não clicar deve ser negativo.

**Hipótese avaliada:** O remetente pede que o destinatário clique em um link ou botão, ou abra um endereço de internet.

- Positivo esperado: Clique no link abaixo para atualizar seu cadastro imediatamente.
- Negativo esperado: https://exemplo.com

### `solicita_ligacao`

Número de telefone isolado e comando para ligar um aparelho não equivalem a telefonar.

**Hipótese avaliada:** O remetente pede que o destinatário faça uma ligação telefônica.

- Positivo esperado: Para confirmar o cancelamento, ligue imediatamente para 0800 123 4567.
- Negativo esperado: Telefone: (19) 99999-1234.

### `menciona_bloqueio_conta`

Detecta estado atual ou futuro. Bloqueio de rua e cancelamento de pedido não são o objeto desta feature.

**Hipótese avaliada:** A mensagem afirma que a conta, cartão, cadastro, acesso ou serviço do destinatário está ou será bloqueado, suspenso ou cancelado.

- Positivo esperado: Sua conta será bloqueada hoje caso você não confirme seus dados.
- Negativo esperado: Sua conta não será bloqueada.

### `carga_emocional`

Escore semântico do texto inteiro. Não é proporção de palavras emocionais, intensidade psicológica nem apenas sentimento positivo ou negativo.

**Hipótese avaliada:** A mensagem expressa ou tenta provocar emoções como medo, ansiedade, alegria, esperança, raiva ou surpresa.

- Positivo esperado: URGENTE!!! Você pode perder todo o seu dinheiro! Resolva AGORA antes que seja tarde!!!
- Negativo esperado: Seu código é 123456.

### `possui_urgencia`

Distingue pressão temporal de uma simples data, como uma entrega que ocorreu hoje.

**Hipótese avaliada:** A mensagem pressiona o destinatário a agir rapidamente ou dentro de um prazo muito curto.

- Positivo esperado: Regularize sua conta imediatamente. Você tem somente até hoje.
- Negativo esperado: Sua compra foi entregue hoje.

### `possui_ameaca`

Exige consequência condicionada à ação ou omissão. Conta já bloqueada pode ser aviso sem ameaça.

**Hipótese avaliada:** A mensagem ameaça uma consequência negativa para o destinatário caso ele não realize uma ação solicitada.

- Positivo esperado: Caso você não atualize seus dados hoje, sua conta será bloqueada.
- Negativo esperado: Sua conta está bloqueada.

### `possui_linguagem_alarmista`

Alarmismo não é sinônimo de prazo curto. Caixa alta e exclamações isoladas não definem a categoria.

**Hipótese avaliada:** A mensagem usa um tom de alarme ou perigo para assustar ou causar preocupação no destinatário.

- Positivo esperado: ALERTA MÁXIMO! Detectamos uma atividade suspeita em sua conta. Resolva imediatamente!
- Negativo esperado: Atualize imediatamente.

### `possui_recompensa`

Busca benefício oferecido ao destinatário; uma notícia sobre prêmio de outra pessoa é controle negativo.

**Hipótese avaliada:** A mensagem afirma que o destinatário ganhou ou pode resgatar um prêmio, recompensa, brinde ou bônus.

- Positivo esperado: Parabéns! Seu número foi sorteado e você ganhou um prêmio de R$ 5.000. Clique aqui para resgatar.
- Negativo esperado: O prêmio foi entregue ao João.

### `possui_reembolso`

Política geral de reembolso ou pedido negado não equivale a valor disponível.

**Hipótese avaliada:** A mensagem informa que o destinatário tem reembolso, restituição ou devolução de dinheiro disponível para receber.

- Positivo esperado: Identificamos um reembolso de R$ 350,00 disponível para você. Clique aqui para receber.
- Negativo esperado: O reembolso foi negado.

### `possui_vantagem_inesperada`

Infere indícios no texto; não conhece a expectativa real do destinatário. Salário habitual não é vantagem inesperada.

**Hipótese avaliada:** A mensagem oferece ao destinatário um benefício inesperado, uma seleção especial ou uma vantagem extraordinária não solicitada.

- Positivo esperado: Você foi selecionado para receber um benefício de R$ 1.500 que já está disponível para saque.
- Negativo esperado: Seu salário foi depositado.

### `possui_oferta_financeira`

Distingue oferta comercial de simples comprovante ou aviso de parcela paga.

**Hipótese avaliada:** A mensagem oferece crédito, empréstimo, financiamento ou oportunidade de investimento ao destinatário.

- Positivo esperado: Seu crédito de R$ 20.000 foi pré-aprovado. Clique aqui para contratar agora.
- Negativo esperado: Seu dinheiro foi recebido.

### `possui_chamada_acao`

Categoria ampla que pode coexistir com clique, pagamento e envio de dados. Relato no passado e proibição não são pedidos afirmativos.

**Hipótese avaliada:** O remetente solicita que o destinatário realize uma ação concreta.

- Positivo esperado: Informe seu CPF e clique no botão abaixo para confirmar.
- Negativo esperado: Nunca compartilhe sua senha.

### `possui_url`

Retorna 1 se linkify-it-py extrair ao menos uma URL aceita por nossa validação de host/IP. `Acesse https://exemplo.com` é positivo; `pessoa@exemplo.com` é negativo. Reconhece HTTP(S), www, domínios sem esquema e links com `//`; não resolve DNS nem verifica reputação.

### `possui_url_encurtada`

Retorna 1 se o host real de um link estiver em `bit.ly`, `tinyurl.com`, `t.co`, `is.gd` ou `ow.ly`. `https://bit.ly/a` é positivo; `https://bit.ly.exemplo.com/a` é negativo. `usuario@host` é interpretado pelo host, não pelo usuário. Novos serviços precisam ser incluídos em `_urls.py`.

### `possui_telefone`

Retorna 1 se PhoneNumberMatcher encontrar ao menos um telefone estruturalmente válido. `(19) 99999-1234` é positivo; `CPF: 19999991234` é negativo devido à máscara de identificador. Não implica que alguém esteja solicitando uma ligação.

### `possui_pix`

Retorna 1 para a palavra PIX com limites Unicode, ignorando maiúsculas. `Recebemos seu PIX` é positivo; `pixel` é negativo. Detecta menção ao meio de pagamento, mesmo sem solicitação. URLs são mascaradas.

### `possui_erros_ortografia_gramatica`

Retorna 1 se LanguageTool pt-BR apontar ao menos um erro ortográfico ou gramatical. `Sua conta foi bloquiada` é um exemplo de grafia a verificar; `Sua conta foi bloqueada` é um controle. As regras e sugestões são expostas em `detectar_erros()`. A quantidade de apontamentos não é uma medida validada de qualidade textual.

## Verificar e avaliar

```bash
python -m unittest classificador_features_sms.features_bibliotecas.test_bibliotecas -v
python -m classificador_features_sms.features_bibliotecas.avaliar_exemplos > avaliacao_exemplos.json
```

O primeiro comando usa as bibliotecas reais de URL, telefone e regex, com NLI e corretor simulados para testar contrato, falhas, limiares, ordenação e posições. O segundo executa **o NLI real** em 38 exemplos didáticos (um positivo e um negativo por feature semântica) e registra acertos/erros, escores e revisão. Ele não chama o corretor Java. Esses exemplos não substituem um conjunto independente de SMS anotados por humanos. Não ajuste e avalie limiares sobre as mesmas mensagens.

Veja `VALIDACAO.md` para os testes efetivamente executados na criação desta pasta.

## Fontes das bibliotecas e do modelo

- [Transformers: pipeline de classificação zero-shot](https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.ZeroShotClassificationPipeline).
- [Cartão do modelo mDeBERTa multilíngue](https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli).
- [phonenumbers: documentação e exemplos](https://github.com/daviddrysdale/python-phonenumbers).
- [linkify-it-py: documentação](https://linkify-it-py.readthedocs.io/en/latest/).
- [language-tool-python: uso local e requisitos](https://pypi.org/project/language-tool-python/).
- [regex: propriedades Unicode](https://pypi.org/project/regex/).
