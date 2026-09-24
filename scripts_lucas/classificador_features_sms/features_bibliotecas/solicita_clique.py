"""Ter URL não basta. Conselho para não clicar deve ser negativo.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Clique no link abaixo para atualizar seu cadastro imediatamente.
Contraexemplo: https://exemplo.com
"""

HIPOTESE = 'O remetente pede que o destinatário clique em um link ou botão, ou abra um endereço de internet.'
EXPLICACAO = 'Ter URL não basta. Conselho para não clicar deve ser negativo.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('solicita_clique', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
