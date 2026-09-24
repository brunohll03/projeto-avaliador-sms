"""Inclui finalidade de um comando de acesso. Informar que o cadastro está desatualizado não é necessariamente um pedido.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Seu cadastro está desatualizado. Acesse o link abaixo para confirmar seus dados.
Contraexemplo: Cadastro atualizado.
"""

HIPOTESE = 'O remetente pede que o destinatário atualize, confirme ou regularize seu cadastro ou seus dados cadastrais.'
EXPLICACAO = 'Inclui finalidade de um comando de acesso. Informar que o cadastro está desatualizado não é necessariamente um pedido.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('solicita_atualizacao_cadastro', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
