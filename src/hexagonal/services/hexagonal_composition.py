from typing import Optional, List

from hexagonal.domain.hexagonal_layer import HexagonalLayer


class HexagonalComposition(List[HexagonalLayer]):

    def __add__(self, next_layer) -> 'HexagonalComposition':
        self.clear()
        self.append(next_layer)
        return self

    def __rshift__(self, next_layer: HexagonalLayer) -> 'HexagonalComposition':
        self.append(next_layer)
        return self
