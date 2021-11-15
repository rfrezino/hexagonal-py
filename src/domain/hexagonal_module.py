from dataclasses import dataclass
from typing import Optional


@dataclass
class HexagonalModule:
    layer_index: Optional[int]
    module: str
    layer_name: str
