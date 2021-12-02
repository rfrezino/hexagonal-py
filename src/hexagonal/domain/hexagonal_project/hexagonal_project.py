from dataclasses import dataclass
from typing import List

from hexagonal.domain.hexagonal_project.hexagonal_project_layer import HexagonalProjectLayer
from hexagonal.domain.python_file import PythonFile


@dataclass
class HexagonalProject:
    project_path: str
    layers: List[HexagonalProjectLayer]
    files_not_in_layers: List[PythonFile]
