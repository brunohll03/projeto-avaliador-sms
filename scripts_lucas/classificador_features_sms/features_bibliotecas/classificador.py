"""Orquestra 24 features, compartilhando uma única instância do modelo NLI."""

import atexit
from importlib import import_module

from ._gramatica import Corretor
from ._semantica import MotorSemantico
from ._texto import validar
from ._urls import ENCURTADORES, mascarar_urls, ocorrencias
from .config import Configuracao
from .possui_telefone import extrair_telefones
from .possui_pix import classificar as detectar_pix

VERSAO_METODO = "2.0.0-bibliotecas"
NOMES = (
    "solicita_senha", "solicita_codigo_autenticacao", "solicita_dados_bancarios",
    "solicita_dados_pessoais", "solicita_dados_cartao", "solicita_atualizacao_cadastro",
    "solicita_pagamento", "solicita_clique", "solicita_ligacao", "menciona_bloqueio_conta",
    "carga_emocional", "possui_urgencia", "possui_ameaca", "possui_linguagem_alarmista",
    "possui_recompensa", "possui_reembolso", "possui_vantagem_inesperada",
    "possui_oferta_financeira", "possui_url", "possui_url_encurtada", "possui_telefone",
    "possui_pix", "possui_erros_ortografia_gramatica", "possui_chamada_acao",
)
MODULOS = tuple(import_module(f"{__package__}.{nome}") for nome in NOMES)
HIPOTESES = {nome: m.HIPOTESE for nome, m in zip(NOMES, MODULOS) if hasattr(m, "HIPOTESE")}


class ClassificadorFeatures:
    """Use uma instância por processo; close encerra o servidor Java local.

    motor e corretor podem ser fornecidos para testes de integração do contrato.
    Os escores são calculados a cada SMS, sem cache de dados do usuário.
    """

    def __init__(self, config=None, *, motor=None, corretor=None):
        self.config = config or Configuracao()
        desconhecidas = set(self.config.limiares) - HIPOTESES.keys()
        if desconhecidas:
            raise ValueError(f"Limiares só se aplicam às features semânticas: {sorted(desconhecidas)}")
        self.motor = motor if motor is not None else MotorSemantico(self.config)
        self.corretor = corretor if corretor is not None else Corretor(self.config.versao_languagetool)

    def _medida(self, nome, escore):
        limiar = self.config.limiar_de(nome)
        return {"valor": int(escore >= limiar), "escore": escore,
                "limiar": limiar, "hipotese": HIPOTESES[nome],
                "metodo": "NLI zero-shot multilabel; escore não calibrado"}

    def medir_feature(self, nome: str, sms: str) -> dict:
        validar(sms)
        if nome not in HIPOTESES:
            raise ValueError(f"Feature semântica desconhecida: {nome}")
        # Emoção não deve ser inferida de palavras no caminho/domínio de URLs.
        texto = mascarar_urls(sms) if nome == "carga_emocional" else sms
        escore = self.motor.escores(texto, {nome: HIPOTESES[nome]})[nome]
        return self._medida(nome, escore)

    def analisar_sms(self, sms: str) -> dict:
        validar(sms)
        escores = {nome: 0.0 for nome in HIPOTESES}
        urls, telefones, erros = [], [], []
        pix = 0
        if sms.strip():
            # Mantém URLs nos pedidos de clique; emoção recebe texto mascarado.
            outras = {nome: h for nome, h in HIPOTESES.items() if nome != "carga_emocional"}
            escores.update(self.motor.escores(sms, outras))
            escores.update(self.motor.escores(mascarar_urls(sms),
                                             {"carga_emocional": HIPOTESES["carga_emocional"]}))
            urls = ocorrencias(sms)
            telefones = extrair_telefones(sms)
            pix = detectar_pix(sms)
            erros = self.corretor.detectar_erros(sms)
        semanticas = {nome: self._medida(nome, escore) for nome, escore in escores.items()}
        valores = {nome: m["valor"] for nome, m in semanticas.items()}
        valores.update(possui_url=int(bool(urls)),
                       possui_url_encurtada=int(any(m["dominio"] in ENCURTADORES for m in urls)),
                       possui_telefone=int(bool(telefones)), possui_pix=pix,
                       possui_erros_ortografia_gramatica=int(bool(erros)))
        return {
            "versao_metodo": VERSAO_METODO,
            "features": {nome: valores[nome] for nome in NOMES},
            "detalhes": {"semanticas": semanticas, "urls": urls, "telefones": telefones,
                         "quantidade_erros": len(erros), "erros_detectados": erros,
                         "carga_emocional": semanticas["carga_emocional"]},
            "configuracao": {"modelo": self.config.modelo,
                             "revisao_solicitada": self.config.revisao,
                             "revisao_carregada": self.motor.revisao_carregada,
                             "languagetool": self.config.versao_languagetool,
                             "idioma_corretor": "pt-BR"},
        }

    def classificar_sms(self, sms: str) -> dict[str, int]:
        return self.analisar_sms(sms)["features"]

    def close(self):
        self.corretor.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


_padrao = None


def obter_classificador() -> ClassificadorFeatures:
    global _padrao
    if _padrao is None:
        _padrao = ClassificadorFeatures()
        atexit.register(_padrao.close)
    return _padrao


def classificar_sms(sms: str) -> dict[str, int]:
    return obter_classificador().classificar_sms(sms)


def analisar_sms(sms: str) -> dict:
    return obter_classificador().analisar_sms(sms)
