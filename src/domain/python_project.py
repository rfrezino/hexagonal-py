from dataclasses import dataclass
from typing import List

from domain.python_file import PythonFile


@dataclass
class PythonProject:
    full_path: str
    python_files: List[PythonFile]
