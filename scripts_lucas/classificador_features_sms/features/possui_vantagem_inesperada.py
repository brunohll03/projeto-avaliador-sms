"""Indícios explícitos de benefício extraordinário ou seleção inesperada."""

from ..regras import afirmacao
from .possui_recompensa import classificar as tem_recompensa


def classificar(sms: str) -> int:
    # O SMS não permite saber a expectativa real da pessoa; esta é uma aproximação.
    return tem_recompensa(sms) or afirmacao(sms,
        r"(?:dinheiro|beneficio)(?:\s+[\w$.,]+){0,7}\s+(?:liberado|disponivel)|"
        r"credito inesperado|desconto extraordinario|oportunidade exclusiva|"
        r"(?:valor|reembolso|credito) surpresa|sem (?:voce )?ter solicitado"
    )
