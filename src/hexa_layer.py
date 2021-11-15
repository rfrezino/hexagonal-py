from dataclasses import dataclass
from typing import List

hexagonal_composition: List['HexagonalLayer'] = []


@dataclass
class HexagonalLayer:
    name: str
    directories: List[str]

    @staticmethod
    def clear():
        hexagonal_composition.clear()

    def __rshift__(self, next_layer: 'HexagonalLayer') -> 'HexagonalLayer':
        if not hexagonal_composition:
            hexagonal_composition.append(self)
            hexagonal_composition.append(next_layer)
        elif self in hexagonal_composition:
            index_self = hexagonal_composition.index(self) + 1
            hexagonal_composition.insert(index_self, next_layer)
        else:
            hexagonal_composition.append(self)
            hexagonal_composition.append(next_layer)

        return hexagonal_composition[-1]
