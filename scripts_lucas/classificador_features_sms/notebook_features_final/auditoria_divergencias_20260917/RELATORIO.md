# Auditoria das divergências — 17/09/2026

## Escopo e limites

Triagem das **4260 divergências salvas**, em 24 features e 1.347 SMS, com o PDF como referência. Leitura individual completa das **121 divergências de autenticação**; nas demais features foram examinados padrões, exemplos de diferentes posições do CSV, regras e efeitos das mudanças. Não se afirma que todas as 4.260 linhas foram julgadas individualmente. Casos pendentes estão explicitamente separados.

O dataset original e o gabarito dos 144 testes não foram alterados. Sugestões desta auditoria não foram gravadas nos campos de decisão humana. A fonte foi conferida por SHA-256. Resultados e código anteriores estão arquivados nesta pasta.

## Código de autenticação

- **110 prováveis erros originais:** entrega/informa código, ou proíbe o envio, sem solicitação de uso/informação.
- **11 falhas do script corrigidas:** dez pedidos de uso/informação antes perdidos e um falso positivo em “Atualize seu token de segurança”.
- “Seu código de verificação é 123456” → 0.
- “Use o código 123456 para autenticação” → 1.
- “Envie o código de 6 dígitos que chegou no celular” → 1.
- “Nunca envie seu código” → 0.
- O rótulo mede solicitação, não malícia: usar código em login legítimo também pode contar.

Estes números são sobre as divergências dessa feature, não a taxa de erro de todos os seus rótulos. A distinção entre pedido de uso e simples entrega segue a página 3 do PDF; interpretações continuam disponíveis para sua contestação.

## Revisão por feature

| Feature | Divergências antes | Depois | Critério e decisão |
|---|---:|---:|---|
| solicita_senha | 13 | 13 | Mantida a revisão anterior: atualizar senha conta; aviso, negação e pedido de bloquear acesso não bastam. Elipse “Recadastre em...” continua ambígua. |
| solicita_codigo_autenticacao | 121 | 110 | Revisão individual das 121 divergências. 110 prováveis erros originais; 11 falhas do script corrigidas. Entregar código não equivale a solicitá-lo. Use/digite com finalidade de autenticação conta; atualizar token não pede seu valor. |
| solicita_dados_bancarios | 1 | 0 | Incluído pedido interrogativo “qual seu banco?”. Conta genérica e aviso bancário continuam insuficientes. |
| solicita_dados_pessoais | 70 | 51 | Script específico mantido. Algumas saídas salvas ainda não refletiam as correções anteriores de confirma/CPF. Aviso de bloqueio de CPF não pede dado pessoal. |
| solicita_dados_cartao | 19 | 19 | Mantido. Bloquear cartão ou cancelar compra não pede número, validade ou CVV. “Atualize seu cartão” sem especificar dados permanece ambíguo. |
| solicita_atualizacao_cadastro | 66 | 65 | Incluído “confirma seu cadastro”. Atualizar aplicativo/token não equivale a atualizar dados cadastrais. Elipses e pedidos de confirmação de CPF merecem revisão específica. |
| solicita_pagamento | 201 | 170 | Incluído “faz o pagamento/PIX”. Negociação, oferta comercial ou aviso de pagamento pendente não se tornam pedidos de pagamento apenas por mencionar dinheiro. |
| solicita_clique | 472 | 408 | Incluídos veja/saiba/confirma quando há link/site/endereço explícito. URL isolada segue insuficiente; comandos genéricos seguidos de URL continuam dependentes de interpretação. |
| solicita_ligacao | 47 | 13 | Incluídos “me liga” e “evite ... ligando para”. Relato “estou ligando” e ligar aparelho não contam; WhatsApp sozinho não pede chamada telefônica. |
| menciona_bloqueio_conta | 118 | 108 | Incluída desativação de conta/serviço. CNH suspensa e bloqueio judicial do CPF não são automaticamente conta/serviço; não ampliados sem definição. |
| carga_emocional | 627 | 627 | Léxico e limites preservados. Diferença metodológica sem padrão-ouro categórico; não ajustar limiares para copiar rótulos humanos. |
| possui_urgencia | 396 | 361 | Pedidos informais, hj, o quanto antes e contagem regressiva; prazo explícito pode estar em frase adjacente. Excluídos fatos passados com já/hoje e duração de leitura. Persistem limitações de contexto. |
| possui_ameaca | 167 | 167 | Mantida: consequência condicionada à ação/omissão. Aviso de problema já ocorrido não basta. “Evite protesto” e condicionais implícitas permanecem candidatos a revisão, sem ampliar por mera palavra negativa. |
| possui_linguagem_alarmista | 351 | 322 | Incluídas falha de segurança, acesso comprometido, movimentação estranha e problema grave; removido falso positivo no título “Capitalismo da atenção”. Linguagem subjetiva restante exige revisão. |
| possui_recompensa | 116 | 93 | Incluídos vc ganhou, recebeu bônus e prêmio esperando por vc. Oferta de empréstimo e benefício ordinário não equivalem automaticamente a prêmio. |
| possui_reembolso | 16 | 3 | Incluídos reembolso aprovado, direito ao reembolso, solicitar ressarcimento e valor a ser estornado. Devolver Pix de terceiro e devolução já concluída não prometem recebimento futuro. |
| possui_vantagem_inesperada | 149 | 126 | Arquivo mantido; herda as melhorias de recompensa. Expectativa real do destinatário não é observável pelo texto: sinalização continua aproximada. |
| possui_oferta_financeira | 268 | 268 | Mantido. Mensalidade de internet, preço de mercadoria ou desconto comercial não são automaticamente oferta de crédito/investimento. Propostas financeiras sem verbos usuais permanecem limite. |
| possui_url | 7 | 7 | Mantido. Casos sem ponto no host e menção textual Gov.br são escolhas de reconhecimento estrutural; exigir decisão de política antes de alterar. |
| possui_url_encurtada | 142 | 142 | Mantida lista fixa. Domínio curto e caminho curto não provam encurtador. goo.gl e outros serviços fora da lista precisam de validação/versionamento; o PDF dá exemplos, não lista exaustiva. |
| possui_telefone | 24 | 24 | Mantido. Número estrangeiro, <NUMERO> e protocolo não satisfazem telefone brasileiro. Códigos de serviço e telefone dentro de URL precisam de política explícita. |
| possui_pix | 36 | 36 | Mantido. 35 divergências 0→1 têm menção explícita; prováveis erros originais. Avisos de chave cadastrada e Pix recebido também contêm PIX, mesmo sem pedido de pagamento. |
| possui_erros_ortografia_gramatica | 391 | 391 | Método mantido. Não tratar gírias/abreviações como erro automaticamente. Nomes e marcas podem gerar falsos positivos do LanguageTool: validar alerta a alerta. |
| possui_chamada_acao | 442 | 233 | Vocabulário compartilhado ampliado com cancele, bloqueie, reative, veja, simule etc. Faz tempo/faz bolos não são ordens. Comandos em SMS legítimos também contam: feature não significa golpe. |

## Resultado e testes

As divergências passaram de **4260 para 3757**; concordância com o CSV original **88.38%**. Concordância não é acurácia: a referência contém rótulos questionáveis. Mesmo uma divergência nova pode estar correta segundo o PDF.

Passaram os **144 testes sintéticos**, **187 verificações da auditoria** (121 mensagens reais revisadas + 66 contraexemplos/casos de regressão), os testes anteriores de pedidos informais e senha, e os quatro testes de integridade, incluindo 117 casos de regressão anteriores. Os casos usados nas correções não são validação independente.

Foram modificados 11 scripts específicos mais `regras.py`. Alterações na lógica compartilhada também afetam features cujo arquivo permaneceu igual. A comparação “antes” usa os resultados salvos encontrados no início, que incluíam saídas anteriores a algumas correções da conversa; portanto toda diferença numérica não deve ser atribuída exclusivamente a este turno.

## Arquivos para revisão

- `analise_codigo_autenticacao.csv`: 121 pareceres com justificativas e valores sugeridos.
- `triagem_divergencias.csv`: todas as divergências antigas, com categorias claras de análise; pendente não significa rótulo correto.
- `mudancas_resultados.csv`: todas as mudanças entre saídas salvas e novas.
- `resumo_por_feature.csv`: comparação de contagens nas 24 features.
- `casos_revisados.json`: gabarito de regressão da auditoria.
- `analise_divergencias.ipynb`: leitura reproduzível dos resultados da auditoria.
- `gerar_relatorio.py`: regenera os CSVs de auditoria após execução do classificador.

Os resultados atuais e o painel foram atualizados em `../resultados`. O notebook principal e seu HTML podem ainda exibir saídas antigas até nova execução/exportação. Não foi feita inspeção visual do painel no navegador nesta revisão.

## Próximas decisões humanas

Priorizar rótulos sugeridos sem aplicá-los automaticamente. Resolver a política de links sem ponto, menções de domínio e serviços telefônicos curtos; revisar os falsos positivos de LanguageTool; anotar uma amostra nova independente com dois revisores para medir precisão/recall reais. Aumentar concordância com os rótulos antigos não deve orientar essas decisões.

Validação do notebook de auditoria: quatro células executadas em ordem via IPython no mesmo processo e saídas salvas. A criação de kernel Jupyter separado foi impedida pelo bloqueio de portas do ambiente; a classificação e os testes foram executados normalmente pelo Python.
