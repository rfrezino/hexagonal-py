from dataclasses import dataclass
from typing import List

from hexagonal.domain.python_file import PythonFile

@dataclass
class HexagonalProjectLayer:
    index: int
    name: str
    directories: List[str]
    python_files: List[PythonFile]
