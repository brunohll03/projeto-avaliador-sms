"""Verifica alinhamento, métricas e exclusões da avaliação de features."""

import csv
from pathlib import Path
import tempfile
import unittest

from classificador_features_sms.comparar_csv import comparar, salvar_relatorios


class TestCompararCSV(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pasta = Path(self.temp.name)

    def csv(self, nome, linhas, colunas=None):
        caminho = self.pasta / nome
        with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(colunas or ["Mensagem", "possui_pix", "possivel_golpe"])
            escritor.writerows(linhas)
        return caminho

    def test_matriz_e_alinhamento_por_mensagem(self):
        # Um VP, um VN, um FP e um FN: todas as métricas são 0,5.
        ref = self.csv("ref.csv", [["a", 1, 1], ["b", 0, 0], ["c", 0, 0], ["d", 1, 1]])
        res = self.csv("res.csv", [["d", 0, 1], ["c", 1, 0], ["b", 0, 0], ["a", 1, 1]])
        resumo, metricas, diferencas = comparar(ref, res)
        pix = next(m for m in metricas if m["feature"] == "possui_pix")
        for chave in ("VP", "VN", "FP", "FN"):
            self.assertEqual(pix[chave], 1)
        for chave in ("acuracia", "precisao", "revocacao", "f1"):
            self.assertEqual(pix[chave], 0.5)
        self.assertEqual(resumo["mensagens_identicas_nas_features_compativeis"], 2)
        self.assertEqual(resumo["rotulos_possivel_golpe_alterados"], 0)
        self.assertEqual([d["motivo"] for d in diferencas], ["FP", "FN"])

    def test_categorias_vazios_ausencias_e_rotulos(self):
        colunas = ["Mensagem", "possui_pix", "carga_emocional", "possivel_golpe"]
        ref = self.csv("ref.csv", [["a", 1, "Alto", 1], ["b", 0, "Baixo", 0],
                                   ["ausente", 1, "Médio", 1]], colunas)
        res = self.csv("res.csv", [["b", "", 0, 1], ["a", 1, 1, 1],
                                   ["extra", 1, 1, 1]], colunas)
        resumo, metricas, diferencas = comparar(ref, res)
        self.assertEqual(resumo["celulas_avaliadas"], 1)
        self.assertEqual(resumo["acuracia_global_celulas_validas"], 1)
        self.assertEqual(resumo["cobertura_celulas_24_features"], 1 / 72)
        self.assertEqual(resumo["mensagens_ausentes_no_resultado"], 1)
        self.assertEqual(resumo["mensagens_extras_no_resultado"], 1)
        self.assertEqual(resumo["rotulos_possivel_golpe_alterados"], 1)
        emocao = next(m for m in metricas if m["feature"] == "carga_emocional")
        self.assertEqual(emocao["status"], "valores_nao_binarios")
        self.assertIsNone(emocao["acuracia"])
        self.assertEqual(len(diferencas), 4)

    def test_sem_positivos_nao_inventa_precisao_ou_f1(self):
        ref = self.csv("ref.csv", [["a", 0, 0]])
        res = self.csv("res.csv", [["a", 0, 0]])
        _, metricas, _ = comparar(ref, res)
        pix = next(m for m in metricas if m["feature"] == "possui_pix")
        self.assertEqual(pix["acuracia"], 1)
        for chave in ("precisao", "revocacao", "f1"):
            self.assertIsNone(pix[chave])

    def test_rejeita_duplicatas(self):
        ref = self.csv("ref.csv", [["a", 1, 0], ["a", 0, 0]])
        res = self.csv("res.csv", [["a", 1, 0]])
        with self.assertRaisesRegex(ValueError, "mensagem repetida"):
            comparar(ref, res)

    def test_multilinha_e_relatorios_preservam_entradas(self):
        sms = 'Mensagem com "aspas", ponto e vírgula;\ne outra linha.'
        ref = self.csv("ref.csv", [[sms, 1, 0]])
        res = self.csv("res.csv", [[sms, 0, 0]])
        originais = ref.read_bytes(), res.read_bytes()
        resumo, metricas, diferencas = comparar(ref, res)
        pasta = self.pasta / "relatorios"
        salvar_relatorios(pasta, resumo, metricas, diferencas)
        with (pasta / "divergencias.csv").open(encoding="utf-8-sig", newline="") as f:
            self.assertEqual(next(csv.DictReader(f))["Mensagem"], sms)
        self.assertEqual((ref.read_bytes(), res.read_bytes()), originais)

    def test_sem_mensagens_comuns_nao_retorna_acuracia(self):
        ref = self.csv("ref.csv", [["a", 1, 0]])
        res = self.csv("res.csv", [["b", 1, 0]])
        resumo, _, _ = comparar(ref, res)
        self.assertIsNone(resumo["acuracia_global_celulas_validas"])
        self.assertEqual(resumo["cobertura_mensagens_referencia"], 0)


if __name__ == "__main__":
    unittest.main()
