"""Testes de preservação do CSV e de falhas durante o processamento."""

from contextlib import contextmanager, redirect_stderr
import csv
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from classificador_features_sms.classificador import classificar_sms
from classificador_features_sms.classificar_csv import preencher_csv


class TestClassificarCSV(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pasta = Path(self.temp.name)
        self.entrada = self.pasta / "entrada.csv"

    def gravar(self, colunas, registros, delimitador=","):
        with self.entrada.open("w", encoding="utf-8-sig", newline="") as arquivo:
            escritor = csv.writer(arquivo, delimiter=delimitador)
            escritor.writerow(colunas)
            escritor.writerows(registros)

    def test_preserva_texto_rotulo_ordem_e_colunas_extras(self):
        mensagens = ['Informe sua senha, "agora".\nAcesse https://bit.ly/exemplo.', "Recebemos seu PIX.", ""]
        nomes = list(classificar_sms(""))
        colunas = ["Mensagem", *nomes, "possivel_golpe", "identificador"]
        registros = [[sms, *([""] * 24), str(i % 2), f"00{i}"]
                     for i, sms in enumerate(mensagens)]
        self.gravar(colunas, registros, ";")
        with redirect_stderr(io.StringIO()):
            self.assertEqual(preencher_csv(self.entrada), 3)
        self.assertTrue(self.entrada.read_bytes().startswith(b"\xef\xbb\xbf"))
        with self.entrada.open(encoding="utf-8-sig", newline="") as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=";")
            self.assertEqual(leitor.fieldnames, colunas)
            for i, linha in enumerate(leitor):
                self.assertEqual(linha["Mensagem"], mensagens[i])
                self.assertEqual(linha["possivel_golpe"], str(i % 2))
                self.assertEqual(linha["identificador"], f"00{i}")
                self.assertEqual({nome: int(linha[nome]) for nome in nomes},
                                 classificar_sms(mensagens[i]))

    def test_saida_separada_e_adicao_de_cabecalhos(self):
        self.gravar(["Mensagem"], [["Recebemos seu PIX."]])
        original = self.entrada.read_bytes()
        saida = self.pasta / "saida.csv"
        with redirect_stderr(io.StringIO()):
            preencher_csv(self.entrada, saida)
        self.assertEqual(self.entrada.read_bytes(), original)
        with saida.open(encoding="utf-8-sig", newline="") as arquivo:
            linha = next(csv.DictReader(arquivo))
        self.assertEqual(len(linha), 25)
        self.assertEqual(linha["possui_pix"], "1")

    def test_falha_no_meio_preserva_saida_e_remove_temporario(self):
        self.gravar(["Mensagem"], [["primeira"], ["segunda"]])
        original = self.entrada.read_bytes()
        resultados = [classificar_sms(""), RuntimeError("modelo indisponível")]

        @contextmanager
        def backend(*args):
            def classificar(sms):
                resultado = resultados.pop(0)
                if isinstance(resultado, Exception):
                    raise resultado
                return resultado
            yield tuple(classificar_sms("")), classificar

        with patch("classificador_features_sms.classificar_csv.abrir_classificador", backend):
            with redirect_stderr(io.StringIO()):
                with self.assertRaisesRegex(RuntimeError, "registro 2"):
                    preencher_csv(self.entrada)
        self.assertEqual(self.entrada.read_bytes(), original)
        self.assertEqual(list(self.pasta.iterdir()), [self.entrada])

    def test_rejeita_linha_incompleta_sem_alterar_arquivo(self):
        self.gravar(["Mensagem", "possivel_golpe"], [["faltou campo"]])
        original = self.entrada.read_bytes()
        with self.assertRaisesRegex(ValueError, "Registro 1"):
            preencher_csv(self.entrada)
        self.assertEqual(self.entrada.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
