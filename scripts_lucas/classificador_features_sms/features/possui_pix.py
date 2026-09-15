"""Referência explícita ao PIX, independentemente de haver pedido de pagamento."""

from ..regras import contem, normalizar


def classificar(sms: str) -> int:
    # Limites de palavra evitam marcar "pixel" ou "pixar".
    return int(contem(normalizar(sms), r"pix"))
