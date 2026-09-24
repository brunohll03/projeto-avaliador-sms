"""Compara features binárias de um CSV classificado com uma referência anotada."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from classificador_features_sms.classificador import MODULOS
else:
    from .classificador import MODULOS

FEATURES = tuple(modulo.__name__.rsplit(".", 1)[-1] for modulo in MODULOS)


def ler_csv(caminho):
    """Usa o texto exato como chave; duplicatas tornam o alinhamento ambíguo."""
    with Path(caminho).open(encoding="utf-8-sig", newline="") as arquivo:
        cabecalho = arquivo.readline()
        if not cabecalho:
            raise ValueError(f"{caminho}: CSV vazio.")
        dialect = (csv.Sniffer().sniff(cabecalho, delimiters=",;\t")
                   if any(c in cabecalho for c in ",;\t") else csv.excel)
        arquivo.seek(0)
        leitor = csv.reader(arquivo, dialect, doublequote=True, strict=True)
        colunas = next(leitor)
        if len(set(colunas)) != len(colunas) or any(not c for c in colunas):
            raise ValueError(f"{caminho}: cabeçalhos vazios ou repetidos.")
        if "Mensagem" not in colunas:
            raise ValueError(f"{caminho}: falta a coluna Mensagem.")
        registros = {}
        for numero, valores in enumerate(leitor, start=1):
            if len(valores) != len(colunas):
                raise ValueError(f"{caminho}: registro {numero} com número incorreto de campos.")
            registro = dict(zip(colunas, valores))
            mensagem = registro["Mensagem"]
            if not mensagem.strip():
                raise ValueError(f"{caminho}: registro {numero} sem mensagem para alinhar.")
            if mensagem in registros:
                raise ValueError(f"{caminho}: mensagem repetida no registro {numero}; "
                                 "a comparação exige mensagens únicas.")
            registros[mensagem] = (numero, registro)
    return colunas, registros


def dividir(numerador, denominador):
    return numerador / denominador if denominador else None


def comparar(referencia, resultado):
    colunas_ref, ref = ler_csv(referencia)
    colunas_res, res = ler_csv(resultado)
    comuns = [sms for sms in ref if sms in res]
    metricas, divergencias = [], []

    def registrar(sms, feature, motivo, esperado="", obtido=""):
        divergencias.append({
            "registro_referencia": ref[sms][0] if sms in ref else "",
            "registro_resultado": res[sms][0] if sms in res else "",
            "Mensagem": sms, "feature": feature, "motivo": motivo,
            "referencia": esperado, "resultado": obtido,
        })

    for sms in (sms for sms in ref if sms not in res):
        registrar(sms, "", "mensagem_ausente_no_resultado")
    for sms in (sms for sms in res if sms not in ref):
        registrar(sms, "", "mensagem_ausente_na_referencia")

    # Uma coluna categórica não é convertida nem parcialmente avaliada como binária.
    elegiveis = []
    for nome in FEATURES:
        faltantes = [origem for origem, colunas in (("referencia", colunas_ref),
                                                   ("resultado", colunas_res))
                     if nome not in colunas]
        valores_ref = sorted({r[nome] for _, r in ref.values()}) if nome in colunas_ref else []
        valores_res = sorted({r[nome] for _, r in res.values()}) if nome in colunas_res else []
        incompativel = any(v.strip() not in ("", "0", "1") for v in valores_ref + valores_res)
        status = ("coluna_ausente_em_" + "_e_".join(faltantes) if faltantes
                  else "valores_nao_binarios" if incompativel else "ok")
        linha = {"feature": nome, "status": status, "pares_alinhados": len(comuns),
                 "avaliados": 0, "nao_avaliados": len(comuns), "cobertura": 0.0 if comuns else None,
                 "acertos": 0, "erros": 0, "VP": 0, "VN": 0, "FP": 0, "FN": 0,
                 "positivos_referencia": 0, "acuracia": None, "precisao": None,
                 "revocacao": None, "f1": None,
                 "valores_referencia": json.dumps(valores_ref, ensure_ascii=False),
                 "valores_resultado": json.dumps(valores_res, ensure_ascii=False)}
        metricas.append(linha)
        if status != "ok":
            continue
        elegiveis.append(nome)
        contagens = Counter()
        for sms in comuns:
            esperado = ref[sms][1][nome].strip()
            obtido = res[sms][1][nome].strip()
            if not esperado or not obtido:
                registrar(sms, nome, "valor_vazio", esperado, obtido)
                continue
            chave = {("1", "1"): "VP", ("0", "0"): "VN",
                     ("0", "1"): "FP", ("1", "0"): "FN"}[(esperado, obtido)]
            contagens[chave] += 1
            if esperado != obtido:
                registrar(sms, nome, chave, esperado, obtido)
        vp, vn, fp, fn = (contagens[chave] for chave in ("VP", "VN", "FP", "FN"))
        n = vp + vn + fp + fn
        linha.update(status="ok" if n else "sem_pares_validos", avaliados=n,
                     nao_avaliados=len(comuns) - n, cobertura=dividir(n, len(comuns)),
                     acertos=vp + vn, erros=fp + fn, VP=vp, VN=vn, FP=fp, FN=fn,
                     positivos_referencia=vp + fn, acuracia=dividir(vp + vn, n),
                     precisao=dividir(vp, vp + fp), revocacao=dividir(vp, vp + fn),
                     f1=dividir(2 * vp, 2 * vp + fp + fn))

    rotulos_alterados = None
    if "possivel_golpe" in colunas_ref and "possivel_golpe" in colunas_res:
        rotulos_alterados = 0
        for sms in comuns:
            esperado, obtido = ref[sms][1]["possivel_golpe"], res[sms][1]["possivel_golpe"]
            if esperado != obtido:
                rotulos_alterados += 1
                registrar(sms, "possivel_golpe", "rotulo_alterado", esperado, obtido)

    completos, identicos = 0, 0
    for sms in comuns:
        a, b = ref[sms][1], res[sms][1]
        if elegiveis and all(a[n].strip() in ("0", "1") and b[n].strip() in ("0", "1")
                            for n in elegiveis):
            completos += 1
            identicos += all(a[n].strip() == b[n].strip() for n in elegiveis)
    total = sum(m["avaliados"] for m in metricas)
    resumo = {
        "referencia": str(Path(referencia).resolve()), "resultado": str(Path(resultado).resolve()),
        "registros_referencia": len(ref), "registros_resultado": len(res),
        "mensagens_alinhadas": len(comuns), "cobertura_mensagens_referencia": dividir(len(comuns), len(ref)),
        "mensagens_ausentes_no_resultado": len(ref.keys() - res.keys()),
        "mensagens_extras_no_resultado": len(res.keys() - ref.keys()),
        "features_binarias_compativeis": elegiveis,
        "features_nao_avaliadas": {m["feature"]: m["status"] for m in metricas if not m["avaliados"]},
        "celulas_avaliadas": total,
        "cobertura_celulas_24_features": dividir(total, len(ref) * len(FEATURES)),
        "acuracia_global_celulas_validas": dividir(sum(m["acertos"] for m in metricas), total),
        "mensagens_completas_nas_features_compativeis": completos,
        "mensagens_identicas_nas_features_compativeis": identicos,
        "taxa_mensagens_identicas_nas_features_compativeis": dividir(identicos, completos),
        "rotulos_possivel_golpe_alterados": rotulos_alterados,
        "observacao": "Concordância com a referência fornecida; sua qualidade depende das anotações. "
                      "Valores ausentes ou não binários não contam como acertos. "
                      "possivel_golpe é verificado apenas para preservação, não como predição. "
                      "Métricas sem denominador são null no JSON e vazias no CSV.",
    }
    return resumo, metricas, divergencias


def salvar_relatorios(pasta, resumo, metricas, divergencias):
    pasta = Path(pasta)
    destinos = [pasta / nome for nome in ("resumo.json", "metricas.csv", "divergencias.csv")]
    entradas = {Path(resumo[chave]).resolve() for chave in ("referencia", "resultado")}
    if any(p.resolve() in entradas for p in destinos):
        raise ValueError("A pasta de saída sobrescreveria um dos CSVs de entrada.")
    pasta.mkdir(parents=True, exist_ok=True)
    destinos[0].write_text(json.dumps(resumo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for destino, registros, colunas in (
        (destinos[1], metricas, list(metricas[0])),
        (destinos[2], divergencias, ["registro_referencia", "registro_resultado", "Mensagem",
                                     "feature", "motivo", "referencia", "resultado"]),
    ):
        with destino.open("w", encoding="utf-8-sig", newline="") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas)
            escritor.writeheader()
            escritor.writerows(registros)


def porcentagem(valor):
    return f"{valor:.2%}" if valor is not None else "n/a"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("referencia", type=Path, help="CSV com as anotações consideradas corretas.")
    parser.add_argument("resultado", type=Path, help="CSV preenchido pelo classificador.")
    parser.add_argument("--saida", type=Path, default=Path("comparacao_csv"),
                        help="Pasta dos relatórios (padrão: comparacao_csv); relatórios anteriores são substituídos.")
    args = parser.parse_args()
    try:
        resumo, metricas, divergencias = comparar(args.referencia, args.resultado)
        salvar_relatorios(args.saida, resumo, metricas, divergencias)
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, f"Erro: {exc}\n")
    print(f"Mensagens alinhadas: {resumo['mensagens_alinhadas']}/{resumo['registros_referencia']}")
    print(f"Ausentes no resultado: {resumo['mensagens_ausentes_no_resultado']}; "
          f"extras: {resumo['mensagens_extras_no_resultado']}")
    print(f"Concordância global (células válidas): {porcentagem(resumo['acuracia_global_celulas_validas'])}")
    print(f"Cobertura das 24 features da referência: {porcentagem(resumo['cobertura_celulas_24_features'])}")
    print(f"Mensagens idênticas nas features compatíveis: "
          f"{resumo['mensagens_identicas_nas_features_compativeis']}/"
          f"{resumo['mensagens_completas_nas_features_compativeis']}")
    print(f"{'Feature':38} {'Acurácia':>9} {'Precisão':>9} {'Revocação':>9} {'F1':>9}")
    for m in metricas:
        print(f"{m['feature']:38} " + " ".join(f"{porcentagem(m[c]):>9}" for c in
              ("acuracia", "precisao", "revocacao", "f1")) +
              (f"  [{m['status']}]" if m["status"] != "ok" else ""))
    print(f"Rótulos possivel_golpe alterados: {resumo['rotulos_possivel_golpe_alterados']}")
    print(f"Relatórios: {args.saida.resolve()}")
    print("Concordância depende da qualidade da referência; consulte também F1, cobertura e divergências.")


if __name__ == "__main__":
    main()
