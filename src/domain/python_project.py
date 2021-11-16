from dataclasses import dataclass
from typing import List

from domain.python_file import PythonFile


@dataclass
class PythonProject:
    python_files: List[PythonFile]
