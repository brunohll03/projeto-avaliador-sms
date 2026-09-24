"""Casos revisados conforme o PDF, sem usar rótulos originais como verdade."""
import json
import unittest
from pathlib import Path
from ..classificador import preparar, MODULOS, ESTRUTURAIS


class AuditoriaDivergencias(unittest.TestCase):
    def test_criterios_revisados(self):
        arquivo = Path(__file__).resolve().parents[1]/'auditoria_divergencias_20260917/casos_revisados.json'
        casos = json.loads(arquivo.read_text())
        for caso in casos:
            with self.subTest(feature=caso['feature'], sms=caso['sms']):
                texto = caso['sms'] if caso['feature'] in ESTRUTURAIS else preparar(caso['sms'])
                self.assertEqual(MODULOS[caso['feature']].classificar(texto), caso['esperado'])


if __name__ == '__main__':
    unittest.main()
