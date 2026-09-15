"""Afirmação de devolução ou valor disponível para recebimento."""

from ..regras import afirmacao


def classificar(sms: str) -> int:
    beneficio = r"reembolso|restituicao|devolucao de dinheiro|credito"
    return afirmacao(sms, rf"(?:{beneficio})(?:\s+[\w$.,]+){{0,9}}\s+disponivel|"
                     rf"(?:voce tem direito a|receba|recebera|receber|liberamos)(?:\s+\w+){{0,4}}\s+(?:{beneficio})|"
                     r"(?:voce tem|identificamos|consta)(?:\s+\w+){0,4}\s+valor(?:es)? a receber")
