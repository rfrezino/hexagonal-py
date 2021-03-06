from dataclasses import dataclass
from typing import List, Optional

from hexagonal.domain.hexagonal_project.hexagonal_project_layer import HexagonalProjectLayer
from hexagonal.domain.python_file import PythonFile


@dataclass
class HexagonalProject:
    project_path: str
    layers: List[HexagonalProjectLayer]
    files_not_in_layers: List[PythonFile]

    def get_layer_for_file_path(self, file_full_path: str) -> Optional[HexagonalProjectLayer]:
        for layer in self.layers:
            if layer.is_file_in_layer(file_full_path=file_full_path):
                return layer
        return None

    def get_python_file(self, file_full_path: str) -> PythonFile:
        for layer in self.layers:
            python_file = layer.get_python_file(file_full_path=file_full_path)
            if python_file:
                return python_file

        raise Exception(f'File not found {file_full_path}')
