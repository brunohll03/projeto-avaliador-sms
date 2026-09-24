"""Combina erros conhecidos e LanguageTool filtrado; preserva a auditoria."""
from ..ortografia_manual import detectar_erros

def analisar(sms, gramatica):
    if gramatica is None:
        raise ValueError('A gramática deve ser calculada pelo motor local; ausência não significa zero.')
    aceitos = list(gramatica['aceitos'])
    for erro in detectar_erros(sms):
        if not any(erro['trecho'].casefold() in e['trecho'].casefold() for e in aceitos):
            aceitos.append({**erro, 'regra':'lista_manual_fixa'})
    return {'aceitos':aceitos, 'ignorados':list(gramatica['ignorados'])}

def classificar(sms, gramatica=None):
    return int(bool(analisar(sms, gramatica)['aceitos']))
