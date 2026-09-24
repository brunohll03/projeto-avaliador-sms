"""Critérios da página 2 do PDF, incluindo limites da atualização de senha."""
import csv
import unittest
from pathlib import Path
from ..classificador import preparar
from ..features.solicita_senha import classificar

PASTA = Path(__file__).resolve().parents[1]


class AtualizacaoSenha(unittest.TestCase):
    def test_atualizacao_e_limites(self):
        positivos = [
            'Altere sua senha.', 'Troque sua senha.', 'Redefina sua senha.',
            'Recadastre sua senha.', 'Você precisa alterar sua senha.',
            'Poderia trocar sua senha?', 'Se não foi você, altere sua senha.',
            'Não reconhece o acesso? Altere sua senha.',
        ]
        negativos = [
            'Nunca envie sua senha ou código recebido por SMS para terceiros.',
            'Não altere sua senha.', 'Sua senha foi alterada.',
            'Troca de senha solicitada. Cancele no link.',
            'Altere suas credenciais.', 'Bloqueie o acesso no link.',
            'Cancele o login.', 'Reative seu aplicativo.',
            'Altere seu cadastro. Sua senha foi bloqueada.',
            'Ele altere sua senha.',
        ]
        for esperado, textos in [(1, positivos), (0, negativos)]:
            for texto in textos:
                with self.subTest(sms=texto):
                    self.assertEqual(classificar(preparar(texto)), esperado)

    def test_seis_casos_sinteticos_existentes(self):
        with (PASTA/'testes/sms_teste.csv').open(encoding='utf-8-sig') as f:
            casos = [r for r in csv.DictReader(f) if r['feature_alvo']=='solicita_senha']
        self.assertEqual(len(casos), 6)
        for r in casos:
            with self.subTest(sms=r['Mensagem']):
                self.assertEqual(classificar(preparar(r['Mensagem'])), int(r['esperado']))

    def test_divergencias_revisadas(self):
        with (PASTA/'resultados/analise_solicita_senha.csv').open(encoding='utf-8-sig') as f:
            casos = list(csv.DictReader(f))
        self.assertEqual(len(casos), 19)
        for r in casos:
            if r['valor_sugerido'] == '':
                continue  # Elipse ambígua permanece para decisão do usuário.
            with self.subTest(registro=r['registro_original']):
                self.assertEqual(classificar(preparar(r['Mensagem'])), int(r['valor_sugerido']))


if __name__ == '__main__':
    unittest.main()
