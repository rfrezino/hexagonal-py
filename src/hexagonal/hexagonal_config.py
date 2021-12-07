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

    def add_inner_layer_with_dirs(self, layer_name: str, directories: List[str]) -> 'HexagonalConfig':
        self._layers.append(HexagonalLayer(name=layer_name, directories_groups=[directories]))
        return self

    def add_inner_layer_with_dirs_groups(self, layer_name: str,
                                         directories_groups: List[List[str]]) -> 'HexagonalConfig':
        self._layers.append(HexagonalLayer(name=layer_name, directories_groups=directories_groups))
        return self

    def clear_layers(self):
        self._layers.clear()

    @property
    def layers(self) -> HexagonalComposition:
        return self._layers


hexagonal_config = HexagonalConfig()
