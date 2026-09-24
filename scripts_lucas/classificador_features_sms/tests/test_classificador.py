"""Verifica exemplos positivos, exclusões e ambiguidades da primeira versão."""

# BIBLIOTECA UTILIZADA: unittest faz parte do Python. Cada assert compara a
# saída observada com a classificação esperada; subTest identifica qual SMS
# falhou dentro de uma tabela. Não requer instalação de ferramenta de testes.
import unittest

from classificador_features_sms import classificar_sms
from classificador_features_sms.classificador import MODULOS, analisar_sms


POSITIVOS = {
    "solicita_senha": "Para confirmar seu cadastro, informe sua senha de acesso no formulário abaixo.",
    "solicita_codigo_autenticacao": "Digite aqui o código de 6 números que você recebeu por SMS para confirmar sua conta.",
    "solicita_dados_bancarios": "Para liberar seu benefício, informe o número do banco, agência e conta.",
    "solicita_dados_pessoais": "Para atualizar seu cadastro, informe seu CPF, nome completo e data de nascimento.",
    "solicita_dados_cartao": "Para receber o reembolso, informe o número do cartão, validade e código de segurança.",
    "solicita_atualizacao_cadastro": "Seu cadastro está desatualizado. Acesse o link abaixo para confirmar seus dados.",
    "solicita_pagamento": "Para evitar o cancelamento do pedido, faça o pagamento de R$ 29,90 ainda hoje.",
    "solicita_clique": "Clique no link abaixo para atualizar seu cadastro imediatamente.",
    "solicita_ligacao": "Para confirmar o cancelamento, ligue imediatamente para 0800 123 4567.",
    "menciona_bloqueio_conta": "Sua conta será bloqueada hoje caso você não confirme seus dados.",
    "carga_emocional": "URGENTE!!! Você pode perder todo o seu dinheiro! Resolva AGORA antes que seja tarde!!!",
    "possui_urgencia": "Regularize sua conta imediatamente. Você tem somente até hoje.",
    "possui_ameaca": "Caso você não atualize seus dados hoje, sua conta será bloqueada.",
    "possui_linguagem_alarmista": "ALERTA MÁXIMO! Detectamos uma atividade suspeita em sua conta. Resolva imediatamente!",
    "possui_recompensa": "Parabéns! Seu número foi sorteado e você ganhou um prêmio de R$ 5.000. Clique aqui para resgatar.",
    "possui_reembolso": "Identificamos um reembolso de R$ 350,00 disponível para você. Clique aqui para receber.",
    "possui_vantagem_inesperada": "Você foi selecionado para receber um benefício de R$ 1.500 que já está disponível para saque.",
    "possui_oferta_financeira": "Seu crédito de R$ 20.000 foi pré-aprovado. Clique aqui para contratar agora.",
    "possui_url": "Acesse https://exemplo.com/atualizar para continuar.",
    "possui_url_encurtada": "Clique aqui para acessar sua conta: https://bit.ly/3ABCxyz",
    "possui_telefone": "Entre em contato pelo telefone (19) 99999-1234.",
    "possui_pix": "Para liberar seu pedido, faça um PIX de R$ 35,00 para a chave abaixo.",
    "possui_erros_ortografia_gramatica": "Sua conta foi bloquiada por atividade suspetia. Atualize seus dados imedi-atamente.",
    "possui_chamada_acao": "Informe seu CPF e clique no botão abaixo para confirmar.",
}

NEGATIVOS = {
    "solicita_senha": ["Nunca compartilhe sua senha.", "Sua senha foi alterada.", "Esqueceu sua senha?", "Não informe sua senha.", "Informe seu CPF e nunca compartilhe sua senha.", "Não solicitamos que informe sua senha.", "Não é necessário informar sua senha."],
    "solicita_codigo_autenticacao": ["Um código será enviado por SMS.", "Seu código de verificação é 123456.", "Informe o código do produto.", "Digite seu código de desconto.", "Informe o código de segurança do cartão."],
    "solicita_dados_bancarios": ["Sua conta está ativa.", "Seu banco confirmou o depósito.", "Informe o número do cartão.", "Acesse sua conta de e-mail."],
    "solicita_dados_pessoais": ["Seu CPF foi atualizado.", "Nunca envie seu CPF.", "Meu nome completo consta no cadastro."],
    "solicita_dados_cartao": ["Seu cartão chegou.", "Informe sua agência e conta bancária.", "Nunca envie seu CVV."],
    "solicita_atualizacao_cadastro": ["Cadastro atualizado.", "Seu cadastro está desatualizado.", "Informe seu CPF."],
    "solicita_pagamento": ["O pagamento foi recebido.", "Recebemos seu PIX.", "Você precisa informar seu CPF.", "Não faça o pagamento."],
    "solicita_clique": ["https://exemplo.com", "Não clique no link.", "Acesse sua conta amanhã.", "O usuário clicou no link."],
    "solicita_ligacao": ["Telefone: (19) 99999-1234.", "Não ligue para este número.", "Ligue o aparelho.", "Entre em contato por e-mail."],
    "menciona_bloqueio_conta": ["Sua conta não será bloqueada.", "Seu pedido foi cancelado.", "O bloqueio da rua continua."],
    "carga_emocional": ["Seu código é 123456.", "", "123 !!!", "https://alerta.com"],
    "possui_urgencia": ["Sua compra foi entregue hoje.", "Não há urgência.", "Acesse quando quiser, sem pressa.", "Você pagou há 2 horas."],
    "possui_ameaca": ["Sua conta está bloqueada.", "O pagamento foi recebido.", "Caso você não atualize, sua conta não será bloqueada."],
    "possui_linguagem_alarmista": ["Atualize imediatamente.", "BOM DIA!!!", "Não há perigo."],
    "possui_recompensa": ["O prêmio foi entregue ao João.", "Você não ganhou o sorteio.", "Não há prêmio disponível."],
    "possui_reembolso": ["O reembolso foi negado.", "Não há reembolso disponível.", "Qual é a política de reembolso?"],
    "possui_vantagem_inesperada": ["Seu salário foi depositado.", "A compra foi realizada.", "O benefício não está disponível."],
    "possui_oferta_financeira": ["Seu dinheiro foi recebido.", "A parcela do empréstimo foi paga.", "Não contrate empréstimo."],
    "possui_url": ["E-mail: pessoa@exemplo.com", "Versão 1.2.3", "http://", "https://invalido", "https://-invalido.com", "nenhum link"],
    "possui_url_encurtada": ["https://bit.ly.exemplo.com/a", "https://exemplo.com/bit.ly", "https://bit.ly@exemplo.com/a", "https://abc.com/a", "meu@bit.ly"],
    "possui_telefone": ["CPF 19999991234", "CPF: 199.999.912-34", "CEP 13000-123", "Código: 19999991234", "R$ 19999991234", "14/09/2026", "123456", "https://exemplo.com/19999991234", "(20) 99999-1234", "1231999999123499"],
    "possui_pix": ["O pixel está apagado.", "Pixar", "123456"],
    "possui_erros_ortografia_gramatica": ["vc pode responder pq preciso disso blz 😊", "Sua conta foi bloqueada.", "https://bloquiada.com", "voce"],
    "possui_chamada_acao": ["Nunca compartilhe sua senha.", "Sua senha foi alterada.", "Telefone: (19) 99999-1234.", "Seu PIX foi recebido."],
}


class TestClassificador(unittest.TestCase):
    def test_exemplos_do_dicionario(self):
        for nome, sms in POSITIVOS.items():
            with self.subTest(feature=nome, sms=sms):
                self.assertEqual(classificar_sms(sms)[nome], 1)

    def test_contraexemplos(self):
        for nome, mensagens in NEGATIVOS.items():
            for sms in mensagens:
                with self.subTest(feature=nome, sms=sms):
                    self.assertEqual(classificar_sms(sms)[nome], 0)

    def test_formatos_e_pedidos(self):
        casos = [
            ("solicita_senha", "Você precisa informar sua senha."),
            ("solicita_senha", "Favor digitar sua senha."),
            ("solicita_senha", "Nunca compartilhe sua senha. Digite sua senha aqui."),
            ("solicita_clique", "Acesse https://exemplo.com."),
            ("solicita_codigo_autenticacao", "Envie seu token."),
            ("solicita_pagamento", "Você precisa pagar o boleto."),
            ("possui_urgencia", "Não perca tempo!"),
            ("possui_ameaca", "Pague agora. Caso contrário, sua conta será suspensa."),
            ("possui_url", "www.exemplo.com"),
            ("possui_url", "https://127.0.0.1:8080/a"),
            ("possui_url_encurtada", "bit.ly/abc"),
            ("possui_erros_ortografia_gramatica", "Sua conta foram bloqueadas."),
        ]
        casos += [("possui_telefone", tel) for tel in (
            "(19) 99999-9999", "19 99999-9999", "+55 19 99999-9999",
            "19999999999", "5519999999999", "(11) 3456-7890", "0800 123 4567",
        )]
        for nome, sms in casos:
            with self.subTest(feature=nome, sms=sms):
                self.assertEqual(classificar_sms(sms)[nome], 1)

    def test_contrato(self):
        self.assertEqual(len(MODULOS), 24)
        self.assertEqual(set(classificar_sms("")), set(POSITIVOS))
        for sms in ["", "Bom dia.", *POSITIVOS.values()]:
            saida = classificar_sms(sms)
            self.assertEqual(len(saida), 24)
            self.assertTrue(all(type(v) is int and v in (0, 1) for v in saida.values()))
        self.assertFalse(any(classificar_sms("").values()))
        for entrada in (None, 123, [], {}):
            with self.subTest(entrada=entrada), self.assertRaises(TypeError):
                classificar_sms(entrada)

    def test_medidas_auxiliares(self):
        resultado = analisar_sms("Medo e alegria. bloquiada suspetia https://exemplo.com https://bit.ly/a")
        detalhes = resultado["detalhes"]
        self.assertEqual(detalhes["quantidade_urls"], 2)
        self.assertEqual(detalhes["quantidade_erros"], 2)
        self.assertEqual(detalhes["carga_emocional"]["proporcao"], 2 / 5)
        self.assertEqual(detalhes["taxa_erros_por_palavra"], 2 / 5)
        self.assertEqual(analisar_sms("")["detalhes"]["carga_emocional"]["proporcao"], 0)

    def test_ajustes_de_contexto(self):
        self.assertEqual(classificar_sms("Informe seu CPF, mas não sua senha.")["solicita_senha"], 0)
        self.assertEqual(classificar_sms("Transfira R$ 20,00 para esta conta.")["solicita_pagamento"], 1)
        self.assertEqual(classificar_sms("Hoje é o prazo final para atualizar o cadastro.")["possui_urgencia"], 1)
        self.assertEqual(classificar_sms("Ative o serviço.")["possui_chamada_acao"], 1)


if __name__ == "__main__":
    unittest.main()
