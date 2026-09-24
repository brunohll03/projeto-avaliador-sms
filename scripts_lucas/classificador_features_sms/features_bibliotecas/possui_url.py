"""Detecta URLs HTTP(S), www e domínios sem esquema com linkify-it-py.

O extrator reconhece limites e pontuação; _urls.py valida o domínio ou IP.
E-mails e esquemas como mailto/ftp são excluídos. Não verifica reputação,
DNS ou segurança. Exemplo: 'Acesse https://exemplo.com' -> 1;
'pessoa@exemplo.com' -> 0. Ofuscações hxxp e [.] não são normalizadas.
"""

from ._urls import extrair_urls


def classificar(sms: str) -> int:
    return int(bool(extrair_urls(sms)))
