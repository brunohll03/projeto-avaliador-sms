"""Distingue autenticação de cupom, código de produto e CVV de cartão; informar um código ao usuário não é solicitar esse código.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Digite aqui o código de 6 números que você recebeu por SMS para confirmar sua conta.
Contraexemplo: Um código será enviado por SMS.
"""

HIPOTESE = 'O remetente pede que o destinatário forneça um código de autenticação, token ou código recebido por SMS ou WhatsApp.'
EXPLICACAO = 'Distingue autenticação de cupom, código de produto e CVV de cartão; informar um código ao usuário não é solicitar esse código.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('solicita_codigo_autenticacao', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
