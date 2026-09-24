"""Infere indícios no texto; não conhece a expectativa real do destinatário. Salário habitual não é vantagem inesperada.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Você foi selecionado para receber um benefício de R$ 1.500 que já está disponível para saque.
Contraexemplo: Seu salário foi depositado.
"""

HIPOTESE = 'A mensagem oferece ao destinatário um benefício inesperado, uma seleção especial ou uma vantagem extraordinária não solicitada.'
EXPLICACAO = 'Infere indícios no texto; não conhece a expectativa real do destinatário. Salário habitual não é vantagem inesperada.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('possui_vantagem_inesperada', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
