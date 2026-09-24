"""Distingue pressão temporal de uma simples data, como uma entrega que ocorreu hoje.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Regularize sua conta imediatamente. Você tem somente até hoje.
Contraexemplo: Sua compra foi entregue hoje.
"""

HIPOTESE = 'A mensagem pressiona o destinatário a agir rapidamente ou dentro de um prazo muito curto.'
EXPLICACAO = 'Distingue pressão temporal de uma simples data, como uma entrega que ocorreu hoje.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('possui_urgencia', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
