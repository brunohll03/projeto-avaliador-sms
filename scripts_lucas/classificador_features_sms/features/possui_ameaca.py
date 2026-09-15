"""Consequência negativa condicionada à ação ou à omissão do destinatário."""

from ..regras import acoes, contem, trechos

CONSEQUENCIA = (
    r"bloquead[oa]|bloqueio|suspens[oa]|suspensao|cancelad[oa]|cancelamento|"
    r"multa|multad[oa]|perdera|perder|perda|restricao|restringid[oa]|negativad[oa]"
)


def classificar(sms: str) -> int:
    for trecho in trechos(sms):
        if not contem(trecho, CONSEQUENCIA):
            continue
        condicao = contem(trecho, r"(?:caso|se) (?:voce )?nao|sob pena de")
        alternativa = contem(trecho, r"senao|caso contrario|ou (?:sua|seu|voce)")
        preventiva = contem(trecho, r"(?:para|e) evitar")
        if condicao or ((alternativa or preventiva) and list(acoes(trecho))):
            # Não transforma garantia explícita de ausência de punição em ameaça.
            if contem(trecho, r"nao (?:sera|vai ser|havera|sofrera|perdera)|sem (?:multa|bloqueio|suspensao)"):
                continue
            return 1
    # A condição pode iniciar a frase seguinte: "Pague. Caso contrário, ...".
    partes = trechos(sms)
    for anterior, atual in zip(partes, partes[1:]):
        if atual.startswith(("caso contrario", "senao")) and list(acoes(anterior)):
            if contem(atual, CONSEQUENCIA) and not contem(atual, r"nao|sem"):
                return 1
    return 0
