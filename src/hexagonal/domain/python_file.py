from dataclasses import dataclass
from typing import Optional, List

from hexagonal.domain.python_module import PythonModule


@dataclass
class PythonFile:
    full_path: str
    relative_path_from_source_module: str
    layer_name: str
    layer_index: Optional[int]
    imported_modules: List[PythonModule]
