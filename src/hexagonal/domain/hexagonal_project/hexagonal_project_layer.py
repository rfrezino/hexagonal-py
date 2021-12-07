from dataclasses import dataclass
from typing import List, Optional

from hexagonal.domain.python_file import PythonFile


@dataclass
class HexagonalProjectLayer:
    index: int
    name: str
    directories_groups: List[List[str]]
    python_files: List[PythonFile]

    def get_python_file(self, file_full_path: str) -> Optional[PythonFile]:
        for python_file in self.python_files:
            if python_file.file_full_path == file_full_path:
                return python_file
        return None

    def is_file_in_layer(self, file_full_path: str) -> bool:
        if self.get_python_file(file_full_path=file_full_path):
            return True
        return False
