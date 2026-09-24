"""Reconhecimento conservador de números brasileiros, com DDD ou 0800 etc."""

# BIBLIOTECA UTILIZADA: re é o mecanismo de expressões regulares do Python.
# Primeiro ele identifica candidatos com fronteiras numéricas; depois conferimos
# DDD, quantidade de dígitos e prefixo de fixo/celular. CPF, CNPJ, datas, CEP,
# dinheiro, códigos identificados e URLs são mascarados antes dessa procura.
# Não consultamos operadoras: validade estrutural não prova que a linha exista.
import re

from ..regras import normalizar
from ..urls import extrair_urls

DDDS = frozenset((
    "11 12 13 14 15 16 17 18 19 21 22 24 27 28 "
    "31 32 33 34 35 37 38 41 42 43 44 45 46 47 48 49 "
    "51 53 54 55 61 62 63 64 65 66 67 68 69 "
    "71 73 74 75 77 79 81 82 83 84 85 86 87 88 89 "
    "91 92 93 94 95 96 97 98 99"
).split())


def extrair_telefones(sms: str) -> list[str]:
    texto = normalizar(sms)
    for url in extrair_urls(sms):
        texto = texto.replace(normalizar(url), " ")
    # Máscaras evitam que um trecho de outro identificador vire telefone.
    mascaras = (
        r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
        r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",
        r"\b\d{5}-\d{3}\b",
        r"\b\d{2}[/-]\d{2}[/-]\d{2,4}\b",
        r"(?:r\$|us\$|brl)\s*[\d.,]+",
        r"\b[\d.,]+\s*(?:reais|centavos)\b",
        r"\b(?:cpf|cnpj|cep|codigo|token|pedido|protocolo|boleto|conta|agencia)"
        r"\s*(?:numero|n[ºo.]|e|:)?\s*[:#-]?\s*\d[\d ./-]*",
    )
    for padrao in mascaras:
        texto = re.sub(padrao, " ", texto)
    padrao = (
        r"(?<![\w+./-])(?:\+?55[ -]?)?"
        r"(?:\(\d{2}\)|\d{2})[ .-]?\d{4,5}[ -]?\d{4}(?![\w/-])|"
        r"(?<![\w+./-])0(?:800|300|303|900)[ -]?\d{3}[ -]?\d{4}(?![\w/-])"
    )
    encontrados = []
    for item in re.finditer(padrao, texto):
        digitos = re.sub(r"\D", "", item.group())
        if len(digitos) in (12, 13) and digitos.startswith("55"):
            digitos = digitos[2:]
        if len(digitos) == 11 and digitos.startswith(("0800", "0300", "0303", "0900")):
            encontrados.append(item.group())
        elif digitos[:2] in DDDS:
            local = digitos[2:]
            if (len(local) == 8 and local[0] in "2345") or (len(local) == 9 and local[0] == "9"):
                encontrados.append(item.group())
    return encontrados


def classificar(sms: str) -> int:
    return int(bool(extrair_telefones(sms)))
