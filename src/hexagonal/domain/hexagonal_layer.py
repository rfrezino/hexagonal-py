from dataclasses import dataclass
from typing import List


@dataclass
class HexagonalLayer:
    name: str
    directories: List[str]
