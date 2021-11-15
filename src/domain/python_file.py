import dataclasses
from typing import Optional


@dataclasses.dataclass
class PythonFile:
    file_name: str
    full_path: str
    relative_path_from_source_module: str
    module_name: str
    layer_index: Optional[int]
