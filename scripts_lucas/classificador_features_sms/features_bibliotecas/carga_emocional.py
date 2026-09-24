"""Escore semântico do texto inteiro. Não é proporção de palavras emocionais, intensidade psicológica nem apenas sentimento positivo ou negativo.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: URGENTE!!! Você pode perder todo o seu dinheiro! Resolva AGORA antes que seja tarde!!!
Contraexemplo: Seu código é 123456.
"""

HIPOTESE = 'A mensagem expressa ou tenta provocar emoções como medo, ansiedade, alegria, esperança, raiva ou surpresa.'
EXPLICACAO = 'Escore semântico do texto inteiro. Não é proporção de palavras emocionais, intensidade psicológica nem apenas sentimento positivo ou negativo.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('carga_emocional', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
