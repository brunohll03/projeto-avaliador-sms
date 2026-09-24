"""Uso: python -m classificador_features_sms.main 'Informe seu CPF.'"""

# BIBLIOTECAS UTILIZADAS: argparse lê argumentos e gera --help e mensagens
# de erro; json serializa o resultado em formato legível por outros programas;
# sys fornece a entrada padrão (stdin) e a saída do processo. pathlib representa
# caminhos de forma portável. Todas pertencem ao Python e funcionam localmente.
# O ajuste de sys.path abaixo permite executar tanto `python -m ...main` a
# partir da raiz quanto `python classificador_features_sms/main.py` diretamente.
import argparse
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from classificador_features_sms.classificador import analisar_sms, classificar_sms
else:
    from .classificador import analisar_sms, classificar_sms


def main() -> None:
    parser = argparse.ArgumentParser(description="Classifica as 24 features de um SMS em 0 ou 1.")
    parser.add_argument("sms", nargs="?", help="Mensagem entre aspas; '-' lê todo o texto de stdin.")
    parser.add_argument("--detalhes", action="store_true", help="Inclui medidas emocionais, erros e quantidade de URLs.")
    args = parser.parse_args()
    if args.sms == "-" or (args.sms is None and not sys.stdin.isatty()):
        sms = sys.stdin.read()
    elif args.sms is None:
        sms = input("Digite o SMS: ")
    else:
        sms = args.sms
    resultado = analisar_sms(sms) if args.detalhes else classificar_sms(sms)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
