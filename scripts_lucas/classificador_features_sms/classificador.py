"""Ponto único de classificação; preserva os nomes e a ordem do dicionário."""

from .features import (
    solicita_senha, solicita_codigo_autenticacao, solicita_dados_bancarios,
    solicita_dados_pessoais, solicita_dados_cartao, solicita_atualizacao_cadastro,
    solicita_pagamento, solicita_clique, solicita_ligacao, menciona_bloqueio_conta,
    carga_emocional, possui_urgencia, possui_ameaca, possui_linguagem_alarmista,
    possui_recompensa, possui_reembolso, possui_vantagem_inesperada,
    possui_oferta_financeira, possui_url, possui_url_encurtada, possui_telefone,
    possui_pix, possui_erros_ortografia_gramatica, possui_chamada_acao,
)
from .regras import normalizar
from .urls import extrair_urls

MODULOS = (
    solicita_senha, solicita_codigo_autenticacao, solicita_dados_bancarios,
    solicita_dados_pessoais, solicita_dados_cartao, solicita_atualizacao_cadastro,
    solicita_pagamento, solicita_clique, solicita_ligacao, menciona_bloqueio_conta,
    carga_emocional, possui_urgencia, possui_ameaca, possui_linguagem_alarmista,
    possui_recompensa, possui_reembolso, possui_vantagem_inesperada,
    possui_oferta_financeira, possui_url, possui_url_encurtada, possui_telefone,
    possui_pix, possui_erros_ortografia_gramatica, possui_chamada_acao,
)
VERSAO_REGRAS = "1.0.0"


def classificar_sms(sms: str) -> dict[str, int]:
    """Recebe texto e devolve exatamente as 24 features com inteiros 0 ou 1."""
    normalizar(sms)  # None, números e listas são erros de entrada, não SMS vazios.
    return {modulo.__name__.rsplit(".", 1)[-1]: int(modulo.classificar(sms))
            for modulo in MODULOS}


def analisar_sms(sms: str) -> dict[str, object]:
    """Acrescenta medidas auxiliares sem mudar a representação binária padrão."""
    features = classificar_sms(sms)
    emocional = carga_emocional.medir(sms)
    erros = possui_erros_ortografia_gramatica.detectar_erros(sms)
    total = emocional["palavras_analisaveis"]
    return {
        "versao_regras": VERSAO_REGRAS,
        "features": features,
        "detalhes": {
            "quantidade_urls": len(extrair_urls(sms)),
            "carga_emocional": emocional,
            "quantidade_erros": len(erros),
            "taxa_erros_por_palavra": len(erros) / total if total else 0.0,
            "erros_detectados": erros,
        },
    }
