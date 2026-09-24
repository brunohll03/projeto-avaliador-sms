"""Reconhece links de serviços conhecidos após extração com linkify-it-py.

Compara o host real à lista ENCURTADORES de _urls.py. Não mede comprimento
nem segue redirecionamentos. 'https://bit.ly/a' -> 1;
'https://bit.ly.exemplo.com/a' e 'https://bit.ly@exemplo.com/a' -> 0.
Um serviço fora da lista não será detectado, mesmo se encurtar URLs.
"""

from ._urls import ENCURTADORES, ocorrencias


def classificar(sms: str) -> int:
    return int(any(m['dominio'] in ENCURTADORES for m in ocorrencias(sms)))
