"""Presença estrutural de URL; não avalia se o endereço é malicioso."""

from ..urls import extrair_urls


def classificar(sms: str) -> int:
    # A extração e a validação do domínio são explicadas no arquivo urls.py.
    return int(bool(extrair_urls(sms)))
