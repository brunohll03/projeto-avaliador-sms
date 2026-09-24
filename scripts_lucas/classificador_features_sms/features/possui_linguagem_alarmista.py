"""Vocabulário explícito de perigo, preocupação ou gravidade."""

from ..regras import afirmacao


def classificar(sms: str) -> int:
    # Caixa alta e exclamações isoladas não bastam, nem apenas "imediatamente".
    return afirmacao(sms, r"atencao|alerta(?: maximo)?|risco (?:imediato|iminente)|"
                     r"situacao (?:grave|critica)|(?:voce esta em |sua conta esta em )?perigo|"
                     r"atividade suspeita|fraude detectada|emergencia")
