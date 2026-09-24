"""Regressão de pedidos informais; não altera o gabarito dos 144 SMS."""
import unittest
from ..features.solicita_senha import classificar
from ..features.solicita_dados_pessoais import classificar as dados_pessoais


class PedidosInformais(unittest.TestCase):
    def test_cadastre_se(self):
        for sms, esperado in [
            ('Cadastre-se com seu CPF', 1),
            ('Cadastre-se usando seu e-mail', 1),
            ('Cadastre-se', 0),
            ('Não cadastre-se com seu CPF', 0),
            ('Nunca cadastre-se usando seu e-mail', 0),
        ]:
            with self.subTest(sms=sms):
                self.assertEqual(dados_pessoais(sms), esperado)

    def test_confirmacao_cpf(self):
        casos = [
            ('confirma seu cpf', 1),
            ('confirme seu cpf', 1),
            ('Insira seu CPF', 1),
            ('Altere seu CPF', 1),
            ('Não confirma seu CPF', 0),
            ('Seu CPF foi confirmado', 0),
            ('Seu CPF', 0),
            ('O atendente confirma seu CPF', 0),
        ]
        for sms, esperado in casos:
            with self.subTest(sms=sms):
                self.assertEqual(dados_pessoais(sms), esperado)

    def test_pedido_senha(self):
        for sms in (
            'Me manda a sua senha',
            'Me manda sua senha',
            'Manda sua senha',
            'Me envia sua senha',
            'Me mande sua senha',
            'Me envie sua senha',
            'prezado cliente. me manda sua senha. tem uma movimentação estranha aq. sua conta pode ser bloqueada',
        ):
            with self.subTest(sms=sms):
                self.assertEqual(classificar(sms), 1)

    def test_negacao_mencao_e_relato(self):
        for sms in (
            'Não me manda sua senha',
            'Nunca me envia sua senha',
            'Não manda sua senha',
            'Sua senha foi alterada',
            'Me manda o comprovante. Sua senha foi alterada.',
            'Ele manda sua senha',
            'Me manda seu CPF e nunca compartilhe sua senha',
        ):
            with self.subTest(sms=sms):
                self.assertEqual(classificar(sms), 0)

    def test_pedido_dados_compartilha_vocabulario(self):
        self.assertEqual(dados_pessoais('Me manda seu CPF'), 1)
        self.assertEqual(dados_pessoais('Não me manda seu CPF'), 0)


if __name__ == '__main__':
    unittest.main()
