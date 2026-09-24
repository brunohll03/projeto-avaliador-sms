"""Proporção de palavras de um léxico emocional local fixo, convertido em 0/1."""

# MÉTODO UTILIZADO: léxico manual local, versão 1, sem bibliotecas de IA.
# Este vocabulário é uma aproximação inicial, não o LIWC nem um léxico validado.
# re tokeniza palavras alfabéticas depois da normalização descrita em regras.py.
# Cada ocorrência presente no conjunto abaixo conta uma vez no numerador;
# o denominador é o total de palavras (números e URLs são desconsiderados).
# A saída binária é 1 quando há pelo menos uma ocorrência emocional (taxa > 0).
# Isso representa presença lexical, não intensidade alta nem sentimento negativo.
# Não criamos faixas arbitrárias de baixa/média/alta. A função medir preserva
# a proporção original para análise e posterior validação do léxico.
import re

from ..regras import normalizar
from ..urls import extrair_urls

LEXICO_EMOCIONAL = frozenset({
    "medo", "perigo", "perigoso", "perigosa", "panico", "terror", "ameaca",
    "preocupacao", "preocupado", "preocupada", "ansiedade", "ansioso", "ansiosa",
    "triste", "tristeza", "raiva", "odio", "desespero", "desesperado", "desesperada",
    "alegria", "alegre", "feliz", "felicidade", "amor", "carinho", "esperanca",
    "surpresa", "surpreso", "surpresa", "vergonha", "culpa", "confianca",
    "parabens", "urgente", "urgencia", "alerta", "grave", "risco", "perder", "perda",
})


def medir(sms: str) -> dict[str, object]:
    texto = sms
    for url in extrair_urls(sms):
        texto = texto.replace(url, " ")
    palavras = re.findall(r"\b[a-z]+\b", normalizar(texto))
    emocionais = [p for p in palavras if p in LEXICO_EMOCIONAL]
    return {
        "palavras_analisaveis": len(palavras),
        "ocorrencias_emocionais": len(emocionais),
        "palavras_emocionais": emocionais,
        "proporcao": len(emocionais) / len(palavras) if palavras else 0.0,
    }


def classificar(sms: str) -> int:
    return int(medir(sms)["ocorrencias_emocionais"] > 0)
