"""Alegação de prêmio, seleção ou benefício concedido ao destinatário."""

from ..regras import afirmacao


def classificar(sms: str) -> int:
    return afirmacao(sms, r"voce (?:ganhou|foi (?:selecionad[oa]|sortead[oa]|premiad[oa]))|"
                     r"seu numero foi sorteado|"
                     r"(?:seu|sua) (?:premio|recompensa|brinde|bonus|presente)(?:\s+\w+){0,4}\s+(?:disponivel|liberad[oa])|"
                     r"(?:ganhou|recebera|ganhe|resgate)(?:\s+\w+){0,4}\s+(?:premio|recompensa|brinde|bonus|presente)")
