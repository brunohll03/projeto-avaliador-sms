"""Executa NLI REAL em exemplos didáticos e mostra erros para revisão.

Não usa os exemplos para treinar nem calibrar. São só 2 casos por feature;
o resultado não estima precisão/recall em SMS reais. Para medir generalização,
prepare um conjunto independente anotado e separado do ajuste de hipóteses.
"""

import argparse
import json
from pathlib import Path

from . import ClassificadorFeatures, Configuracao


def main():
    parser = argparse.ArgumentParser(description='Avaliação didática do NLI real; não mede generalização.')
    parser.add_argument('--modelo', default=Configuracao().modelo)
    parser.add_argument('--revisao', default=Configuracao().revisao)
    parser.add_argument('--limiar', type=float, default=0.70)
    parser.add_argument('--somente-local', action='store_true')
    args = parser.parse_args()
    definicoes = json.loads(Path(__file__).with_name('_definicoes.json').read_text())
    resultados = []
    config = Configuracao(modelo=args.modelo, revisao=args.revisao,
                          limiar=args.limiar, somente_local=args.somente_local)
    with ClassificadorFeatures(config) as c:
        for nome, item in definicoes.items():
            for campo, esperado in (('positivo', 1), ('negativo', 0)):
                medida = c.medir_feature(nome, item[campo])
                resultados.append({'feature': nome, 'sms': item[campo], 'esperado': esperado,
                                   'observado': medida['valor'], 'escore': medida['escore'],
                                   'acertou': medida['valor'] == esperado})
        saida = {'aviso': 'Exemplos didáticos; não é avaliação de generalização.',
                 'modelo': c.config.modelo, 'revisao': c.motor.revisao_carregada,
                 'limiar': c.config.limiar, 'total': len(resultados),
                 'acertos': sum(r['acertou'] for r in resultados), 'resultados': resultados}
    print(json.dumps(saida, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
