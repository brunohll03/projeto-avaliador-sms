# Revisão das 24 features

Base: Dicionário de Features, páginas 2–25. Versão anterior preservada.

Nas features de intenção, motor comum mantém negação, mascara URLs, reconhece pedidos polidos e distingue telefone substantivo de verbo. Acrescenta confira/conferir e negocie/negociar.

Os textos foram revisados por critério; os rótulos originais não foram usados como autoridade para corrigir regras. Casos sintéticos são contratos de desenvolvimento e não evidência independente de desempenho em produção.

## solicita_senha — PDF p. 2

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Pedido explícito de senha de acesso.

**Limites:** Uma confirmação de troca de senha ou orientação para não compartilhar não é solicitação.

## solicita_codigo_autenticacao — PDF p. 3

**Decisão:** ajustado. Acrescenta pedidos de código recebido/enviado por SMS ou WhatsApp; conserva exclusão de códigos de produto e cartão.

**Definição:** Pedido de código de autenticação, token ou verificação recebido por SMS/WhatsApp.

**Limites:** Código de produto ou cupom não conta; código de segurança do cartão pertence à feature de cartão.

## solicita_dados_bancarios — PDF p. 4

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Pedido de banco, agência, número da conta ou dados bancários.

**Limites:** Conta ativa e conta de e-mail não são pedidos de dados bancários.

## solicita_dados_pessoais — PDF p. 5

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Pedido de identificação ou contato: CPF, RG, nome completo, nascimento, endereço, telefone ou e-mail.

**Limites:** CPF apenas mencionado não basta. Listas e construções não previstas podem não ser reconhecidas.

## solicita_dados_cartao — PDF p. 6

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Pedido de número, validade, CVV/CVC, nome impresso ou código de segurança do cartão.

**Limites:** Aviso de entrega do cartão não é solicitação; pedido de agência não pertence a esta feature.

## solicita_atualizacao_cadastro — PDF p. 7

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Pedido para atualizar, confirmar, regularizar ou completar cadastro/dados.

**Limites:** Cadastro desatualizado é um estado; sem pedido não ativa esta feature.

## solicita_pagamento — PDF p. 8

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Pedido de pagamento, transferência, depósito, quitação ou PIX.

**Limites:** Recebemos seu PIX é confirmação, não pedido; PIX e pagamento são features diferentes.

## solicita_clique — PDF p. 9

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Comando para clicar/acessar/tocar link, botão ou endereço apresentado.

**Limites:** Link sozinho não ativa a feature; não clique também não. Acesso sem destino explícito é tratado conservadoramente.

## solicita_ligacao — PDF p. 10

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Pedido de ligação telefônica ao destinatário.

**Limites:** Número de telefone sozinho e contato por e-mail não são pedido de ligação.

## menciona_bloqueio_conta — PDF p. 11

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Menção a bloqueio, suspensão ou cancelamento de conta, cartão, cadastro, serviço ou acesso.

**Limites:** Bloqueio de rua ou cancelamento de pedido não contam; negação explícita de bloqueio é excluída nesta operacionalização.

## carga_emocional — PDF p. 12

**Decisão:** ajustado. Preserva proporção lexical e cria baixa/média/alta pelos tercis positivos congelados, sem usar as categorias anotadas.

**Definição:** Proporção de ocorrências de palavras emocionais entre palavras analisáveis.

**Limites:** Faixas relativas à distribuição lexical deste corpus, não níveis psicológicos validados; léxico limitado, sem contexto de negação/ironia. A proporção numérica é preservada.

## possui_urgencia — PDF p. 13

**Decisão:** ajustado. Acrescenta prazos curtos por extenso (uma, duas, três, quatro, seis, doze e vinte e quatro horas); mantém exigência de ação e exclusão de relatos.

**Definição:** Pressão para agir rapidamente ou antes de prazo próximo.

**Limites:** Compra entregue hoje é relato. Uma data passada não implica urgência; datas livres e prazos escritos por extenso têm cobertura limitada.

## possui_ameaca — PDF p. 14

**Decisão:** ajustado. Amplia consequências explícitas com protesto e negativação, mantendo a exigência de condição e exclusão de garantias negativas.

**Definição:** Consequência negativa explicitamente condicionada à ação ou omissão do destinatário.

**Limites:** Sua conta está bloqueada não contém por si só condição. Condicionais longas ou implícitas exigem revisão humana.

## possui_linguagem_alarmista — PDF p. 15

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Vocabulário explícito de gravidade, perigo, medo ou alerta.

**Limites:** Maiúsculas, exclamações e imediatamente sozinhos não bastam. Atenção também pode ser um aviso legítimo.

## possui_recompensa — PDF p. 16

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Alegação de prêmio, brinde ou benefício que o destinatário ganhou, ganhará ou pode resgatar por seleção/contato.

**Limites:** Um prêmio entregue a outra pessoa ou um sorteio não ganho não contam.

## possui_reembolso — PDF p. 17

**Decisão:** ajustado. Exige devolução/restituição/estorno; crédito disponível isolado deixa de ser reembolso. Aceita estorno liberado.

**Definição:** Alegação de devolução, restituição, estorno ou valor anteriormente pago disponível ao destinatário.

**Limites:** Política de reembolso, reembolso negado e oferta de empréstimo não são devoluções.

## possui_vantagem_inesperada — PDF p. 18

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Indício textual de benefício extraordinário, seleção inesperada ou oportunidade exclusiva.

**Limites:** A expectativa real da pessoa é desconhecida. É uma aproximação textual com sobreposição a recompensa e oferta.

## possui_oferta_financeira — PDF p. 19

**Decisão:** ajustado. Reconhece produto financeiro pré-aprovado com espaço/hífen e sem possessivo, mantendo exclusão de simples preço.

**Definição:** Proposta de crédito, empréstimo, financiamento, investimento ou ganho financeiro.

**Limites:** Preço de pacote de internet ou mercadoria não é automaticamente oferta financeira. Alguns rótulos originais podem seguir interpretação mais ampla.

## possui_url — PDF p. 20

**Decisão:** ajustado. Usa extrator linkify-it-py com validação estrutural do host; mantém presença separada de solicitação de clique.

**Definição:** Presença de URL reconhecível na mensagem.

**Limites:** E-mail isolado não conta. Não abre o link nem avalia reputação; novas terminações de domínio podem escapar.

## possui_url_encurtada — PDF p. 21

**Decisão:** ajustado. Usa o mesmo extrator de URL e comparação exata com lista fixa de cinco domínios, sem confundir caminho ou subdomínio.

**Definição:** URL cujo domínio pertence à lista fixa de serviços encurtadores.

**Limites:** URL curta não significa encurtador. bit.ly.exemplo.com não é bit.ly. A lista limitada não cobre todos os serviços existentes.

## possui_telefone — PDF p. 22

**Decisão:** ajustado. Exige validade BR e mascara identificadores, inclusive código de autenticação/verificação/acesso/segurança; rejeita +44.

**Definição:** Presença de telefone brasileiro em formato reconhecível.

**Limites:** Validade estrutural não confirma linha ativa. Identificadores sem rótulo e alguns formatos ambíguos podem causar erros.

## possui_pix — PDF p. 23

**Decisão:** ajustado. Detecta palavra PIX com limites Unicode fora de URLs; continua positiva em negações que mencionam o sistema.

**Definição:** Menção explícita ao sistema PIX.

**Limites:** Chave numérica sozinha não basta. Não faça PIX ainda menciona o sistema; pixel, Pixar e domínio com pix não contam.

## possui_erros_ortografia_gramatica — PDF p. 24

**Decisão:** ajustado. Combina LanguageTool local filtrado com regras manuais já conhecidas; expõe alertas aceitos/ignorados, sem fallback silencioso.

**Definição:** Ao menos um erro identificado por regras ou ferramenta previamente fixadas.

**Limites:** Não pune automaticamente emoji ou falta de pontuação. Nomes/marcas podem gerar falsos positivos. Contagem é de alertas, não necessariamente palavras distintas.

## possui_chamada_acao — PDF p. 25

**Decisão:** arquivo específico preservado. Regra específica mantida: a condição central e as exclusões examinadas correspondem ao dicionário; continua uma heurística com cobertura limitada.

**Definição:** Comando explícito dirigido ao destinatário, como responder, enviar, acessar, ligar ou pagar.

**Limites:** Relatos no passado e orientações negativas não contam. Discurso citado, ironia e escopos longos de negação têm cobertura limitada.

## Histórico dos testes

O gabarito de 144 casos foi escrito antes de executar a nova versão. A primeira rodada acertou 142 casos: falhou no pedido de telefone e no código numérico rotulado como autenticação. As correções trataram essas classes de construção, sem alterar os rótulos esperados. A execução final passou nos 144 casos. O resultado inicial foi mantido em resultados/testes_execucao_inicial.csv.
