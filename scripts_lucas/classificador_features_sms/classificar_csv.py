"""Preenche as features de cada SMS em um CSV usando as regras locais."""

import argparse
from contextlib import contextmanager
import csv
import os
from pathlib import Path
import sys
import tempfile

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from classificador_features_sms.classificador import MODULOS, classificar_sms
else:
    from .classificador import MODULOS, classificar_sms


@contextmanager
def abrir_classificador(metodo):
    """Disponibiliza o classificador de regras, sem dependências externas."""
    if metodo == "regras":
        nomes = tuple(modulo.__name__.rsplit(".", 1)[-1] for modulo in MODULOS)
        yield nomes, classificar_sms
    else:
        raise ValueError(f"Método desconhecido: {metodo}")


def preencher_csv(entrada, saida=None, *, metodo="regras"):
    """Preserva dados e cabeçalhos; substitui a saída somente após concluir."""
    entrada = Path(entrada).resolve()
    saida = Path(saida).resolve() if saida is not None else entrada
    with entrada.open("rb") as arquivo:
        tem_bom = arquivo.read(3) == b"\xef\xbb\xbf"
    with entrada.open(encoding="utf-8-sig", newline="") as arquivo:
        # O cabeçalho identifica CSV separado por vírgula, ponto e vírgula ou tab.
        cabecalho = arquivo.readline()
        if not cabecalho:
            raise ValueError("O CSV está vazio.")
        dialect = (csv.Sniffer().sniff(cabecalho, delimiters=",;\t")
                   if any(separador in cabecalho for separador in ",;\t") else csv.excel)
        arquivo.seek(0)
        leitor = csv.reader(arquivo, dialect, doublequote=True, strict=True)
        colunas = next(leitor)
        if len(colunas) != len(set(colunas)) or any(not nome for nome in colunas):
            raise ValueError("O cabeçalho contém nomes vazios ou repetidos.")
        if "Mensagem" not in colunas:
            raise ValueError("O CSV precisa ter a coluna 'Mensagem'.")
        registros = []
        for numero, valores in enumerate(leitor, start=1):
            if len(valores) != len(colunas):
                raise ValueError(f"Registro {numero}: quantidade de campos diferente do cabeçalho.")
            registros.append(dict(zip(colunas, valores)))

    temporario = None
    try:
        with abrir_classificador(metodo) as (nomes, classificar):
            colunas_saida = colunas + [nome for nome in nomes if nome not in colunas]
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8-sig" if tem_bom else "utf-8", newline="",
                dir=saida.parent, prefix=f".{saida.name}.", suffix=".tmp", delete=False,
            ) as arquivo:
                temporario = Path(arquivo.name)
                escritor = csv.DictWriter(
                    arquivo, fieldnames=colunas_saida, dialect=dialect, doublequote=True,
                    lineterminator="\r\n" if cabecalho.endswith("\r\n") else "\n",
                )
                escritor.writeheader()
                total = len(registros)
                print(f"Método: {metodo}. Mensagens: {total}.", file=sys.stderr)
                for numero, registro in enumerate(registros, start=1):
                    try:
                        resultado = classificar(registro["Mensagem"])
                        if set(resultado) != set(nomes) or any(
                            type(valor) is not int or valor not in (0, 1)
                            for valor in resultado.values()
                        ):
                            raise ValueError("O classificador deve retornar as 24 features com valores 0 ou 1.")
                    except Exception as exc:
                        raise RuntimeError(f"Falha no registro {numero}: {exc}") from exc
                    registro.update(resultado)
                    escritor.writerow(registro)
                    if numero == 1 or numero % 50 == 0 or numero == total:
                        print(f"Classificadas: {numero}/{total}", file=sys.stderr, flush=True)
                arquivo.flush()
                os.fsync(arquivo.fileno())
        os.replace(temporario, saida)
        temporario = None
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)
    return len(registros)


def main():
    parser = argparse.ArgumentParser(
        description="Classifica cada mensagem e preenche as 24 features no CSV. "
                    "Preserva Mensagem, possivel_golpe e outras colunas. "
                    "Por padrão, atualiza o próprio arquivo após concluir.",
    )
    parser.add_argument("csv", type=Path, help="CSV UTF-8 com a coluna Mensagem.")
    parser.add_argument("--saida", type=Path, help="Salva em outro CSV, preservando a entrada.")
    args = parser.parse_args()
    try:
        total = preencher_csv(args.csv, args.saida)
    except (OSError, ValueError, RuntimeError, ImportError, csv.Error) as exc:
        parser.exit(1, f"Erro: {exc}\nO arquivo de saída não foi substituído.\n")
    except KeyboardInterrupt:
        parser.exit(130, "\nInterrompido. O arquivo de saída não foi substituído.\n")
    print(f"Concluído: {total} mensagens. CSV salvo em: {args.saida or args.csv}")


if __name__ == "__main__":
    main()
