from dataclasses import dataclass
from typing import Optional


@dataclass
class PythonFile:
    full_path: str
    relative_path_from_source_module: str
    module_name: str
    layer_index: Optional[int]
