"""Configuração explícita dos modelos; limiares iniciais precisam de validação."""

from dataclasses import dataclass, field
import math


@dataclass(frozen=True)
class Configuracao:
    modelo: str = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
    revisao: str = "main"
    limiar: float = 0.70
    limiares: dict[str, float] = field(default_factory=dict)
    dispositivo: str = "cpu"
    tamanho_lote: int = 8
    somente_local: bool = False
    versao_languagetool: str = "6.8"

    def __post_init__(self):
        for valor in (self.limiar, *self.limiares.values()):
            if not isinstance(valor, (int, float)) or not math.isfinite(valor) or not 0 < valor < 1:
                raise ValueError("Cada limiar deve ser um número finito entre 0 e 1, exclusivo.")
        if type(self.tamanho_lote) is not int or self.tamanho_lote < 1:
            raise ValueError("tamanho_lote deve ser um inteiro positivo.")

    def limiar_de(self, nome: str) -> float:
        return self.limiares.get(nome, self.limiar)
