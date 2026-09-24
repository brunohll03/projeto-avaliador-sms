"""Telefone brasileiro: máscaras + phonenumbers + exigência de região BR."""
import phonenumbers
from ..bibliotecas.possui_telefone import extrair_telefones as candidatos

def extrair_telefones(sms):
    return [trecho for trecho in candidatos(sms)
            if phonenumbers.is_valid_number_for_region(phonenumbers.parse(trecho, 'BR'), 'BR')]

def classificar(sms):
    return int(bool(extrair_telefones(sms)))
