from dataclasses import dataclass
from typing import List

from hexagonal.domain.raw_python_file import RawPythonFile


@dataclass
class PythonFile(RawPythonFile):
    imported_modules: List[str]
