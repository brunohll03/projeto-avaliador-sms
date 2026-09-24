"""Exige consequência condicionada à ação ou omissão. Conta já bloqueada pode ser aviso sem ameaça.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Caso você não atualize seus dados hoje, sua conta será bloqueada.
Contraexemplo: Sua conta está bloqueada.
"""

HIPOTESE = 'A mensagem ameaça uma consequência negativa para o destinatário caso ele não realize uma ação solicitada.'
EXPLICACAO = 'Exige consequência condicionada à ação ou omissão. Conta já bloqueada pode ser aviso sem ameaça.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('possui_ameaca', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
