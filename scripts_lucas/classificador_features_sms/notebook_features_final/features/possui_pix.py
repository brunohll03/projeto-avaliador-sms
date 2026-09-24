"""Referência explícita ao PIX, independentemente de haver pedido de pagamento."""

from ..bibliotecas.possui_pix import classificar as detectar_pix


def classificar(sms: str) -> int:
    # Limites de palavra evitam marcar "pixel" ou "pixar".
    return detectar_pix(sms)
