"""URL com domínio da lista fixa de encurtadores da versão 1."""

from ..urls import ENCURTADORES, dominio, extrair_urls


def classificar(sms: str) -> int:
    # Compara o host real completo; tamanho do link não é critério.
    return int(any(dominio(url) in ENCURTADORES for url in extrair_urls(sms)))
