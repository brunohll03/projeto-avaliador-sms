"""Pedido de identificadores ou dados cadastrais do destinatário."""

from ..regras import solicita


def classificar(sms: str) -> int:
    # Lista editável; confirmações e atualizações explícitas também são pedidos.
    return solicita(sms, r"cpf|rg|nome completo|data de nascimento|endereco|"
                    r"telefone|celular|e-?mail|dados pessoais|dados cadastrais")
