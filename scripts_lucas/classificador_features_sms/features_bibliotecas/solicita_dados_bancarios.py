"""Não confundir conta de e-mail nem simples aviso de depósito com pedido de dados bancários.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Para liberar seu benefício, informe o número do banco, agência e conta.
Contraexemplo: Sua conta está ativa.
"""

HIPOTESE = 'O remetente solicita dados bancários do destinatário, como banco, agência ou número de conta bancária.'
EXPLICACAO = 'Não confundir conta de e-mail nem simples aviso de depósito com pedido de dados bancários.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('solicita_dados_bancarios', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
