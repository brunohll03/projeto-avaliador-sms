"""Dados de cartão são distintos de agência e conta bancária; pode coexistir com pedido de dados pessoais.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Para receber o reembolso, informe o número do cartão, validade e código de segurança.
Contraexemplo: Seu cartão chegou.
"""

HIPOTESE = 'O remetente solicita o número, a validade, o CVV ou outros dados do cartão do destinatário.'
EXPLICACAO = 'Dados de cartão são distintos de agência e conta bancária; pode coexistir com pedido de dados pessoais.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('solicita_dados_cartao', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
