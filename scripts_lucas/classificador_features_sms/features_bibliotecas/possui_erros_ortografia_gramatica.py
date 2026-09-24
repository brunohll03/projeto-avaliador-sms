"""Detecta apontamentos ortográficos/gramaticais do LanguageTool em pt-BR.

O servidor local combina dicionário e regras de concordância, regência etc.
A lista de erros manuais original foi substituída. Filtramos estilo/tipografia
 e expomos regra, posição e sugestões sem corrigir o SMS. Uma ocorrência basta
para 1. Nomes próprios, gírias e abreviações podem gerar falsos positivos;
zero não significa português perfeito. Requer Java 17+ e download inicial.

Exemplo para revisão: 'Sua conta foi bloquiada.'; controle: 'Sua conta foi bloqueada.'
"""


def detectar_erros(sms: str) -> list[dict]:
    from .classificador import obter_classificador
    return obter_classificador().corretor.detectar_erros(sms)


def classificar(sms: str) -> int:
    return int(bool(detectar_erros(sms)))
