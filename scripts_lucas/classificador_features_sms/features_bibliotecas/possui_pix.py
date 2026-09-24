"""Detecta a menção literal PIX usando regex e limites Unicode.

Feature lexical: a palavra basta, inclusive em 'não faça PIX'. Não é pedido
 de pagamento. regex impede coincidências dentro de letras, marcas de acento,
números e sublinhados; assim 'pixel', 'Pixar' e 'meu_pix' não contam. URLs são
mascaradas para o nome de um domínio não virar menção do meio de pagamento.
Um modelo estatístico seria desnecessário para esta definição literal.
"""

from ._texto import validar
from ._urls import mascarar_urls


def classificar(sms: str) -> int:
    validar(sms)
    if not sms.strip():
        return 0
    import regex
    return int(bool(regex.search(r"(?<![\p{L}\p{M}\p{N}_])pix(?![\p{L}\p{M}\p{N}_])",
                                 mascarar_urls(sms), flags=regex.I)))
