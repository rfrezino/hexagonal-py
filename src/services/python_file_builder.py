from domain.python_file import PythonFile
from services.hexagonal_composition import HexagonalComposition


class PythonFileBuilder:
    @staticmethod
    def build(source_module_dir: str, file_full_path: str, composition: HexagonalComposition) -> PythonFile:
        relative_path_from_source_module = file_full_path.replace(source_module_dir + '/', '')
        module_name = relative_path_from_source_module.split('/')[0]

        return PythonFile(file_name='no function used',
                          full_path=file_full_path,
                          relative_path_from_source_module=relative_path_from_source_module,
                          module_name=module_name,
                          layer_index=composition.get_layer_index_by_module_name(module=module_name))
