from typing import Optional

from services.hexagonal_composition import HexagonalComposition


class PythonFile:
    file_name: str
    full_path: str
    relative_path_from_source_module: str
    module_name: str
    layer_index: Optional[int]

    def __init__(self, source_module_dir: str, file_full_path: str, hexagonal_composition: HexagonalComposition):
        self.full_path = file_full_path
        self.relative_path_from_source_module = file_full_path.replace(source_module_dir + '/', '')
        self.module_name = self.relative_path_from_source_module.split('/')[0]
        self.layer_index = hexagonal_composition.get_layer_index_by_module_name(self.module_name)
