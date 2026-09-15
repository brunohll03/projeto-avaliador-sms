"""Pedido de código de autenticação; códigos de produto e cupom não contam."""

from ..regras import contem, solicita, trechos


def classificar(sms: str) -> int:
    for trecho in trechos(sms):
        alvo = r"token|otp|codigo (?:de |do |da )?(?:autenticacao|verificacao|confirmacao|sms|whatsapp|acesso|2fa|dois fatores)"
        # "Código de segurança" com cartão é dado de cartão, não autenticação.
        if not contem(trecho, r"cartao|cvv|cvc"):
            alvo += r"|codigo de seguranca"
        # Aceita "código de 6 números que recebeu por SMS", como no dicionário.
        alvo += r"|codigo de [46] (?:numeros|digitos)(?:\s+\w+){0,7}\s+(?:sms|whatsapp|autenticacao|verificacao)"
        if solicita(trecho, alvo):
            return 1
    return 0
