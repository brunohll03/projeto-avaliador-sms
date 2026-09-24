"""Pressão temporal relacionada a uma ação, não apenas menção a uma data."""

from ..regras import afirmacao, acoes, contem, normalizar


def classificar(sms: str) -> int:
    texto = normalizar(sms)
    if contem(texto, r"nao perca tempo"):
        return 1
    # Indicadores diretos já expressam pressão; "não há urgência" é excluído.
    if afirmacao(sms, r"urgente|urgencia|ultima chance|nao perca tempo"):
        return 1
    if contem(texto, r"sem pressa|nao (?:e |ha )?urgencia"):
        return 0
    if afirmacao(sms, r"(?:hoje|agora)(?:\s+\w+){0,3}\s+prazo final|prazo final(?:\s+\w+){0,3}\s+hoje"):
        return 1
    if not list(acoes(texto)):
        return 0
    return int(contem(texto, r"agora|imediatamente|hoje|ja|em poucos minutos|"
                      r"(?:em|ate|dentro de|prazo de) (?:[1-9]|1[0-9]|2[0-4]) horas?|"
                      r"(?:em|ate|dentro de|prazo de) (?:[1-9]|[1-5][0-9]|60) minutos?"))
