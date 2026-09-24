"""Número de telefone isolado e comando para ligar um aparelho não equivalem a telefonar.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Para confirmar o cancelamento, ligue imediatamente para 0800 123 4567.
Contraexemplo: Telefone: (19) 99999-1234.
"""

HIPOTESE = 'O remetente pede que o destinatário faça uma ligação telefônica.'
EXPLICACAO = 'Número de telefone isolado e comando para ligar um aparelho não equivalem a telefonar.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('solicita_ligacao', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
