"""Solicitação de agência, banco e dados da conta bancária."""

from ..regras import solicita


def classificar(sms: str) -> int:
    # "Conta" sem qualificação também pode ser de e-mail; não é suficiente.
    return solicita(sms, r"(?:numero (?:do |da ))?(?:banco|agencia)|"
                    r"numero (?:da |de )conta|conta bancaria|dados bancarios|"
                    r"dados (?:da |de sua |da sua )conta(?: bancaria)?")
