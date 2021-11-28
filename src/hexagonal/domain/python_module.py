from dataclasses import dataclass
from typing import Optional


@dataclass
class PythonModule:
    layer_index: Optional[int]
    module: str
    layer_name: str
