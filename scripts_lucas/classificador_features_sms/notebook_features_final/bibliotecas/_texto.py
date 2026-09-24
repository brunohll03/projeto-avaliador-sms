"""Validação compartilhada sem carregar bibliotecas ou modelos pesados."""


def validar(sms: str) -> str:
    if not isinstance(sms, str):
        raise TypeError("O SMS deve ser uma string.")
    return sms
