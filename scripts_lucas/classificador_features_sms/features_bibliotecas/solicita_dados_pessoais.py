"""Exige intenção de solicitar; um aviso de CPF atualizado não basta.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: Para atualizar seu cadastro, informe seu CPF, nome completo e data de nascimento.
Contraexemplo: Seu CPF foi atualizado.
"""

HIPOTESE = 'O remetente pede que o destinatário forneça dados pessoais, como CPF, RG, nome completo, endereço ou data de nascimento.'
EXPLICACAO = 'Exige intenção de solicitar; um aviso de CPF atualizado não basta.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('solicita_dados_pessoais', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
