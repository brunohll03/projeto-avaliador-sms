"""PIX recebido é comprovante; não deve ser confundido com pedido para pagar.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Para evitar o cancelamento do pedido, faça o pagamento de R$ 29,90 ainda hoje.
Contraexemplo: O pagamento foi recebido.
"""

HIPOTESE = 'O remetente pede que o destinatário faça um pagamento, depósito ou transferência de dinheiro.'
EXPLICACAO = 'PIX recebido é comprovante; não deve ser confundido com pedido para pagar.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('solicita_pagamento', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
