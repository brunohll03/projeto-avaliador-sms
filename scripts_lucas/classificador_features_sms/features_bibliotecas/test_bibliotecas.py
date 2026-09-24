"""Testes de contrato e extração; não medem qualidade semântica do modelo.

Executar: python -m unittest classificador_features_sms.features_bibliotecas.test_bibliotecas -v
Os extratores usam bibliotecas reais; NLI/Java são simulados neste arquivo.
Para avaliação real de NLI, execute avaliar_exemplos.py, conforme o README.
"""

from types import SimpleNamespace
import json
from pathlib import Path
import unittest
from unittest.mock import Mock

from . import ClassificadorFeatures, Configuracao
from ._gramatica import Corretor
from ._semantica import MotorSemantico
from ._urls import mascarar_urls
from .classificador import HIPOTESES, MODULOS, NOMES
from .possui_pix import classificar as pix
from .possui_telefone import classificar as telefone
from .possui_url import classificar as url
from .possui_url_encurtada import classificar as encurtada


class TestExtratores(unittest.TestCase):
    def test_urls_e_falsos_encurtadores(self):
        for sms in ('https://exemplo.com/a', 'www.exemplo.com', 'bit.ly/abc', 'https://127.0.0.1:8080/a'):
            with self.subTest(sms=sms):
                self.assertEqual(url(sms), 1)
        for sms in ('pessoa@exemplo.com', 'Versão 1.2.3', 'http://', 'https://invalido', 'https://-invalido.com'):
            with self.subTest(sms=sms):
                self.assertEqual(url(sms), 0)
        self.assertEqual(encurtada('https://bit.ly/a'), 1)
        for sms in ('https://bit.ly.exemplo.com/a', 'https://exemplo.com/bit.ly', 'https://bit.ly@exemplo.com/a', 'meu@bit.ly'):
            with self.subTest(sms=sms):
                self.assertEqual(encurtada(sms), 0)

    def test_telefones_e_identificadores(self):
        for sms in ('(19) 99999-1234', '+55 19 99999-1234', '(11) 3456-7890', '0800 123 4567', '+44 20 8366 1177'):
            with self.subTest(sms=sms):
                self.assertEqual(telefone(sms), 1)
        for sms in ('CPF: 19999991234', '199.999.912-34', 'Código: 19999991234',
                    'R$ 19999991234', '(20) 99999-1234', 'https://exemplo.com/19999991234', '14/09/2026'):
            with self.subTest(sms=sms):
                self.assertEqual(telefone(sms), 0)

    def test_pix_unicode(self):
        for sms in ('Faça PIX.', 'Não faça pix!', 'Recebi um Pix.'):
            self.assertEqual(pix(sms), 1)
        for sms in ('pixel', 'Pixar', 'meu_pix', 'pixé', 'pix\u0301', 'https://pix.com'):
            self.assertEqual(pix(sms), 0)

    def test_mascara_preserva_posicoes(self):
        sms = 'Veja https://exemplo.com. Erro bloquiada.'
        texto = mascarar_urls(sms)
        self.assertEqual(len(texto), len(sms))
        self.assertEqual(texto.index('bloquiada'), sms.index('bloquiada'))

    def test_entrada_invalida_e_vazia(self):
        for modulo in MODULOS:
            with self.subTest(modulo=modulo.__name__):
                self.assertEqual(modulo.classificar(''), 0)
                with self.assertRaises(TypeError):
                    modulo.classificar(None)


class TestIntegracaoContrato(unittest.TestCase):
    def test_catalogo_corresponde_aos_modulos(self):
        catalogo = json.loads(Path(__file__).with_name('_definicoes.json').read_text())
        self.assertEqual(len(NOMES), 24)
        self.assertEqual(len(HIPOTESES), 19)
        self.assertEqual({nome: item['hipotese'] for nome, item in catalogo.items()}, HIPOTESES)

    def criar(self, config=None):
        motor = Mock(revisao_carregada='revisao-de-teste')
        motor.escores.side_effect = lambda sms, h: {k: (0.9 if k == 'solicita_senha' else 0.1) for k in h}
        corretor = Mock()
        corretor.detectar_erros.return_value = []
        return ClassificadorFeatures(config, motor=motor, corretor=corretor)

    def test_24_saidas_e_duas_chamadas_compartilhadas(self):
        with self.criar() as c:
            r = c.analisar_sms('Informe sua senha em https://bit.ly/a')
            self.assertEqual(tuple(r['features']), NOMES)
            self.assertTrue(all(type(v) is int and v in (0, 1) for v in r['features'].values()))
            self.assertEqual(r['features']['solicita_senha'], 1)
            self.assertEqual(r['features']['possui_url_encurtada'], 1)
            self.assertEqual(c.motor.escores.call_count, 2)
        c.corretor.close.assert_called_once()

    def test_limiar_individual(self):
        c = self.criar(Configuracao(limiares={'solicita_senha': 0.95}))
        self.assertEqual(c.classificar_sms('Informe sua senha')['solicita_senha'], 0)
        self.assertEqual(c.medir_feature('solicita_senha', 'Informe sua senha')['limiar'], 0.95)

    def test_vazio_sem_carregar_dependencias(self):
        c = self.criar()
        self.assertFalse(any(c.classificar_sms('  \n ').values()))
        c.motor.escores.assert_not_called()
        c.corretor.detectar_erros.assert_not_called()

    def test_falha_nao_vira_zero(self):
        c = self.criar()
        c.corretor.detectar_erros.side_effect = RuntimeError('Java indisponível')
        with self.assertRaisesRegex(RuntimeError, 'Java'):
            c.classificar_sms('Mensagem de teste')

    def test_configuracao_invalida(self):
        for limiar in (0, 1, -1, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                Configuracao(limiar=limiar)
        with self.assertRaises(ValueError):
            ClassificadorFeatures(Configuracao(limiares={'nome_inexistente': 0.5}))

    def test_rotulos_nli_fora_de_ordem(self):
        motor = MotorSemantico(Configuracao())
        pipe = Mock()
        pipe.tokenizer = Mock(return_value={'input_ids': [1, 2, 3]})
        pipe.tokenizer.model_max_length = 512
        pipe.return_value = [
            [{'label': 'neutral', 'score': 0.7}, {'label': 'entailment', 'score': 0.2}, {'label': 'contradiction', 'score': 0.1}],
            [{'label': 'entailment', 'score': 0.9}, {'label': 'neutral', 'score': 0.05}, {'label': 'contradiction', 'score': 0.05}],
        ]
        motor._pipeline = pipe
        self.assertEqual(motor.escores('Texto', {'a': 'Hipótese A', 'b': 'Hipótese B'}), {'a': 0.2, 'b': 0.9})
        self.assertIsNone(pipe.call_args.kwargs['top_k'])
        self.assertEqual(pipe.call_args.kwargs['function_to_apply'], 'softmax')
        pipe.tokenizer.return_value = {'input_ids': list(range(513))}
        with self.assertRaisesRegex(ValueError, 'tokens'):
            motor.escores('Texto grande', {'a': 'Hipótese A'})

    def test_filtro_gramatical_e_offsets(self):
        corretor = Corretor()
        base = dict(offset=0, error_length=9, replacements=['bloqueada'], message='Grafia', rule_id='REGRA')
        corretor._tool = Mock()
        corretor._tool.check.return_value = [
            SimpleNamespace(**base, rule_issue_type='misspelling'),
            SimpleNamespace(**base, rule_issue_type='style'),
        ]
        erros = corretor.detectar_erros('bloquiada')
        self.assertEqual(len(erros), 1)
        self.assertEqual(erros[0]['trecho'], 'bloquiada')
        self.assertEqual(erros[0]['tipo'], 'ortografia')


if __name__ == '__main__':
    unittest.main()
