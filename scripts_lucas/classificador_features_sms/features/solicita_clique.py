"""Comando para abrir link, endereço ou botão mencionado no SMS."""

from ..regras import solicita
from ..urls import extrair_urls


def classificar(sms: str) -> int:
    texto = sms
    # Substitui cada URL por uma marca para pontos do domínio não quebrarem frases.
    for url in extrair_urls(sms):
        texto = texto.replace(url, " endereco_url ")
    return solicita(texto, r"aqui|link|botao|endereco|endereco_url|site|"
                    r"para (?:confirmar|continuar|atualizar|resgatar|receber)",
                    verbos=r"clique|acesse|toque|abra")
