from dataclasses import dataclass
from typing import Optional


@dataclass
class PythonModule:
    layer_index: Optional[int]
    layer_name: str
    module: str
