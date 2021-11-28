import os.path
from modulefinder import ModuleFinder
from typing import List

from domain.python_file import PythonFile
from domain.python_module import PythonModule
from services.hexagonal_composition import HexagonalComposition


class PythonFileBuilder:
    _composition: HexagonalComposition
    _onion_modules_dirs_names: List[str]
    _used_local_modules: List[str]
    _project_full_path: str

    def build(self, *, project_full_path: str, file_full_path: str, composition: HexagonalComposition) -> PythonFile:
        self._composition = composition
        self._project_full_path = project_full_path

        relative_path_from_source_module = file_full_path.replace(project_full_path + '/', '')
        self._used_local_modules = self._get_python_project_local_modules(relative_path_from_source_module)

        layer_name = relative_path_from_source_module.split('/')[0]
        layer_index = composition.get_layer_index_by_module_name(layer_name)
        python_modules = self._get_modules_imported_in_python_file(file_full_path=file_full_path)

        return PythonFile(full_path=file_full_path,
                          relative_path_from_source_module=relative_path_from_source_module,
                          layer_name=layer_name,
                          layer_index=layer_index,
                          imported_modules=python_modules)

    def _get_python_project_local_modules(self, source_folder: str) -> List[str]:
        if '/' not in source_folder:
            return []

        source_dir_name = source_folder.split('/')[-1]
        all_dirs = [source_dir_name]

        for layer in self._composition:
            all_dirs += layer.directories

        return all_dirs

    @staticmethod
    def _convert_bad_modules_into_paths(base_file_full_path: str, bad_modules: List[str]) -> List[str]:
        result = []
        for bad_module in bad_modules:
            bad_module_file = bad_module.replace('.', '/') + '.py'

            connection_string = bad_module_file.split('/')[0]
            base_prefix = base_file_full_path.split(f'/{connection_string}/')[0]
            bad_module_file = base_prefix + '/' + bad_module_file

            if os.path.isfile(bad_module_file):
                result.append(bad_module_file)

        return result

    def _get_all_modules_source_paths(self, file_full_path: str) -> List[str]:
        finder = ModuleFinder(path=[self._project_full_path])
        finder.run_script(file_full_path)

        all_modules = []
        for module in finder.modules.values():
            all_modules.append(module.__file__)

        all_modules.extend(self._convert_bad_modules_into_paths(base_file_full_path=file_full_path,
                                                                bad_modules=list(finder.badmodules.keys())))

        return list(filter(lambda value: value is not None, all_modules))

    def _get_modules_imported_in_python_file(self, *, file_full_path: str) -> List[PythonModule]:
        if not os.path.exists(file_full_path):
            return []

        valid_modules = []
        all_modules = self._get_all_modules_source_paths(file_full_path=file_full_path)

        imported_sources_from_layers = [module for module in all_modules if
                                        any([f'/{valid_dir}/' in module for valid_dir in self._used_local_modules])]

        for imported_source in imported_sources_from_layers:
            hexagonal_module = PythonModule(layer_index=None, module=imported_source, layer_name='')
            self._set_layer_information(hexagonal_module, imported_source)

            if hexagonal_module.layer_index is not None:
                valid_modules.append(hexagonal_module)

        valid_modules.sort(key=lambda valid_module: valid_module.layer_index, reverse=True)
        return valid_modules

    def _set_layer_information(self, hexagonal_module, imported_source):
        if self._project_full_path in imported_source:
            imported_source = imported_source.split(f'{self._project_full_path}/')[1]
        layer_name = imported_source.split('/')[0]
        hexagonal_module.layer_name = layer_name
        hexagonal_module.layer_index = self._composition.get_layer_index_by_module_name(module=layer_name)
