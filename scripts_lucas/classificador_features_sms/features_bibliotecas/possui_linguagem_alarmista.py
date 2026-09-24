"""Alarmismo não é sinônimo de prazo curto. Caixa alta e exclamações isoladas não definem a categoria.

Bibliotecas: Transformers executa a classificação zero-shot com modelo NLI
multilíngue; PyTorch calcula a rede neural. Não há treinamento nestes scripts.
O SMS é comparado à hipótese abaixo e 1 significa escore >= limiar (0,70
inicial). O escore não é calibrado; negação e contexto podem ser interpretados
incorretamente. Os exemplos são expectativas para avaliação, não garantias.

Exemplo positivo: ALERTA MÁXIMO! Detectamos uma atividade suspeita em sua conta. Resolva imediatamente!
Contraexemplo: Atualize imediatamente.
"""

HIPOTESE = 'A mensagem usa um tom de alarme ou perigo para assustar ou causar preocupação no destinatário.'
EXPLICACAO = 'Alarmismo não é sinônimo de prazo curto. Caixa alta e exclamações isoladas não definem a categoria.'


def medir(sms: str) -> dict:
    """Retorna escore, limiar e hipótese usados na decisão."""
    from .classificador import obter_classificador
    return obter_classificador().medir_feature('possui_linguagem_alarmista', sms)


def classificar(sms: str) -> int:
    """Retorna 0 ou 1 pela comparação do escore com o limiar configurado."""
    return medir(sms)["valor"]
