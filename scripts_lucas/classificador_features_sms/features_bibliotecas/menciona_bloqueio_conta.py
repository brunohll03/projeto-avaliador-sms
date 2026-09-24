"""Detecta estado atual ou futuro. Bloqueio de rua e cancelamento de pedido não são o objeto desta feature.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Sua conta será bloqueada hoje caso você não confirme seus dados.
Contraexemplo: Sua conta não será bloqueada.
"""

HIPOTESE = 'A mensagem afirma que a conta, cartão, cadastro, acesso ou serviço do destinatário está ou será bloqueado, suspenso ou cancelado.'
EXPLICACAO = 'Detecta estado atual ou futuro. Bloqueio de rua e cancelamento de pedido não são o objeto desta feature.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('menciona_bloqueio_conta', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
