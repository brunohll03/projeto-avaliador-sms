"""Busca benefício oferecido ao destinatário; uma notícia sobre prêmio de outra pessoa é controle negativo.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Parabéns! Seu número foi sorteado e você ganhou um prêmio de R$ 5.000. Clique aqui para resgatar.
Contraexemplo: O prêmio foi entregue ao João.
"""

HIPOTESE = 'A mensagem afirma que o destinatário ganhou ou pode resgatar um prêmio, recompensa, brinde ou bônus.'
EXPLICACAO = 'Busca benefício oferecido ao destinatário; uma notícia sobre prêmio de outra pessoa é controle negativo.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('possui_recompensa', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
