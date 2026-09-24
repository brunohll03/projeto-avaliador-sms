"""Inferência de linguagem natural (NLI) com Transformers e PyTorch.

Cada SMS é uma premissa, cada definição é uma hipótese. O modelo avalia
apoio (entailment), neutralidade e contradição. Cada par é independente:
um SMS pode pedir senha E impor urgência. Usamos text-classification com
pares de texto para preservar as TRÊS saídas NLI; a pipeline pronta de
zero-shot-classification descartaria a saída neutra no modo multilabel.
O escore é exp(apoio)/soma(exp(logits das três classes)). Ainda não é uma
probabilidade calibrada da feature, nem probabilidade de golpe.
"""

import math

from ._texto import validar
from .config import Configuracao


class MotorSemantico:
    """Carrega o modelo uma vez por instância e não armazena mensagens."""

    def __init__(self, config: Configuracao):
        self.config = config
        self._pipeline = None

    def _carregar(self):
        if self._pipeline is None:
            try:
                from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
            except ImportError as exc:
                raise RuntimeError("Instale as dependências de features_bibliotecas/requirements.txt.") from exc
            opcoes = dict(revision=self.config.revisao,
                          local_files_only=self.config.somente_local,
                          trust_remote_code=False)
            try:
                tokenizer = AutoTokenizer.from_pretrained(self.config.modelo, **opcoes)
                modelo = AutoModelForSequenceClassification.from_pretrained(
                    self.config.modelo, use_safetensors=True, **opcoes)
                rotulos = {str(k).lower() for k in modelo.config.label2id}
                if rotulos != {"entailment", "neutral", "contradiction"}:
                    raise ValueError("O modelo precisa identificar entailment, neutral e contradiction em label2id.")
                self._pipeline = pipeline("text-classification", model=modelo,
                                          tokenizer=tokenizer, device=self.config.dispositivo)
            except (OSError, ImportError) as exc:
                raise RuntimeError("Não foi possível carregar o modelo NLI. Confira instalação, rede e cache; nenhum resultado foi inventado.") from exc
        return self._pipeline

    @property
    def revisao_carregada(self):
        if self._pipeline is None:
            return None
        return getattr(self._pipeline.model.config, "_commit_hash", None)

    def escores(self, sms: str, hipoteses: dict[str, str]) -> dict[str, float]:
        validar(sms)
        if not sms.strip():
            return {nome: 0.0 for nome in hipoteses}
        motor = self._carregar()
        # Rejeitamos textos longos antes de chamar a pipeline para
        # evitar perder um pedido ou uma negação no final sem avisar o usuário.
        limite = min(motor.tokenizer.model_max_length, 512)
        for hipotese in hipoteses.values():
            tokens = motor.tokenizer(sms, hipotese, truncation=False)["input_ids"]
            if len(tokens) > limite:
                raise ValueError(f"SMS e hipótese ultrapassam {limite} tokens. Analise mensagens menores preservando o contexto.")
        pares = [{"text": sms, "text_pair": h} for h in hipoteses.values()]
        resultado = motor(pares, top_k=None, function_to_apply="softmax",
                          truncation=False, batch_size=self.config.tamanho_lote)
        if len(resultado) != len(hipoteses):
            raise RuntimeError("O modelo não devolveu todos os pares SMS/hipótese.")
        # As classes de cada par podem vir ordenadas pelo escore. Identificamos
        # apoio pelo NOME, nunca pela posição. Os pares mantêm a ordem de entrada.
        saida = {}
        for nome, classes in zip(hipoteses, resultado):
            por_classe = {item["label"].lower(): float(item["score"]) for item in classes}
            saida[nome] = por_classe["entailment"]
        if any(not math.isfinite(v) or not 0 <= v <= 1 for v in saida.values()):
            raise RuntimeError("O modelo retornou um escore inválido.")
        return saida
