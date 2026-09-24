"""Terminal: python -m classificador_features_sms.features_bibliotecas.main."""

import argparse
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from classificador_features_sms.features_bibliotecas import ClassificadorFeatures, Configuracao
else:
    from . import ClassificadorFeatures, Configuracao


def main():
    parser = argparse.ArgumentParser(description="Extrai 24 features de um SMS em português com bibliotecas especializadas.")
    parser.add_argument("sms", nargs="?", help="Texto entre aspas, ou '-' para ler stdin.")
    parser.add_argument("--detalhes", action="store_true", help="Inclui hipóteses, escores, limiares e evidências estruturais.")
    parser.add_argument("--limiar", type=float, default=0.70, help="Limiar semântico inicial, não calibrado (padrão: 0.70).")
    parser.add_argument("--somente-local", action="store_true", help="Carrega NLI apenas do cache. LanguageTool precisa estar instalado em cache também.")
    parser.add_argument("--revisao", default="main", help="Commit/revisão do modelo para reproduzir uma execução.")
    args = parser.parse_args()
    if args.sms == "-" or (args.sms is None and not sys.stdin.isatty()):
        sms = sys.stdin.read()
    elif args.sms is None:
        sms = input("Digite o SMS: ")
    else:
        sms = args.sms
    try:
        config = Configuracao(limiar=args.limiar, revisao=args.revisao, somente_local=args.somente_local)
        with ClassificadorFeatures(config) as classificador:
            resultado = classificador.analisar_sms(sms) if args.detalhes else classificador.classificar_sms(sms)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    except (RuntimeError, ImportError, OSError, ValueError) as exc:
        parser.exit(2, f"Erro: {exc}\n")


if __name__ == "__main__":
    main()
