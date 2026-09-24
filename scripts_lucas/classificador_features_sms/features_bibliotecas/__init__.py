"""Cópia com bibliotecas especializadas; não substitui a versão original."""

from .classificador import ClassificadorFeatures, analisar_sms, classificar_sms
from .config import Configuracao

__all__ = ["ClassificadorFeatures", "Configuracao", "analisar_sms", "classificar_sms"]
