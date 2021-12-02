from typing import List

from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.services.hexagonal_composition import HexagonalComposition


class HexagonalConfig:
    excluded_dirs: List[str]
    _layers: HexagonalComposition

    def __init__(self):
        self._layers = HexagonalComposition()
        self.excluded_dirs = []

    def add_inner_layer(self, layer: HexagonalLayer) -> 'HexagonalConfig':
        self._layers.append(layer)
        return self

    def clear_layers(self):
        self._layers.clear()

    @property
    def layers(self) -> HexagonalComposition:
        return self._layers


hexagonal_config = HexagonalConfig()
