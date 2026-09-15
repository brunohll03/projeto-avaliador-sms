"""Pedido explícito de senha, incluindo confirmação e atualização."""

from ..regras import solicita


def classificar(sms: str) -> int:
    # A palavra sozinha não basta: exige verbo de pedido e ignora negações locais.
    return solicita(sms, r"senhas?(?: de acesso)?")
