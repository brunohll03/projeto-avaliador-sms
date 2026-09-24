"""Comando afirmativo dirigido ao destinatário, qualquer que seja a ação."""

from ..regras import acoes, trechos


def classificar(sms: str) -> int:
    # Infinitivos soltos e relatos no passado não são considerados comandos.
    return int(any(list(acoes(trecho)) for trecho in trechos(sms)))
