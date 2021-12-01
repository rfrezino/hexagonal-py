import os.path
from modulefinder import ModuleFinder, Module
from typing import List, Optional

from hexagonal.domain.python_file import PythonFile
from hexagonal.domain.python_module import PythonModule
from hexagonal.services.hexagonal_composition import HexagonalComposition


class PythonFileBuilder:
    _composition: HexagonalComposition
    _onion_modules_dirs_names: List[str]
    _used_local_modules: List[str]
    _project_full_path: str
    # new
    _file_full_path: str
    _file_name: str
    _file_folder: str

    @property
    def file_full_path(self) -> str:
        return self._file_full_path

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def file_folder(self) -> str:
        return self._file_folder

    def __init__(self, file_full_path: str):
        if not file_full_path.startswith('/'):
            raise Exception("The param file_full_path must have the file's full path.")

        if not os.path.isfile(file_full_path):
            raise Exception('Source file not found.')

        if not file_full_path.endswith('.py'):
            raise Exception('File must have .py extension.')

        self._file_full_path = file_full_path
        self._file_name = self._get_file_name_from_full_file_path()
        self._file_folder = self._get_file_folder_path()

    def _get_file_name_from_full_file_path(self) -> str:
        return self._file_full_path.split('/')[-1]

    def _get_file_folder_path(self) -> str:
        return os.path.abspath(self.file_full_path.replace(self.file_name, ''))

    def build(self, *, project_full_path: str, composition: HexagonalComposition) -> PythonFile:
        self._composition = composition
        self._project_full_path = project_full_path

        relative_path_from_source_module = self._file_full_path.replace(project_full_path + '/', '')
        self._used_local_modules = self._get_python_project_local_modules(relative_path_from_source_module)

        layer_name = relative_path_from_source_module.rsplit('/', 1)[0]
        layer_index = composition.get_layer_index_by_module_name(layer_name)
        python_modules = self._get_modules_imported_in_python_file(file_full_path=self._file_full_path)

        return PythonFile(full_path=self._file_full_path,
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

    def __get_module_file_name(self, module: Module) -> Optional[str]:
        string_representation = str(module).strip()
        if not string_representation:
            return None

        try:
            return str(module).split("'")[3]
        except IndexError:
            return None
        except Exception:
            return None

    def _get_all_modules_source_paths(self, file_full_path: str) -> List[str]:
        finder = ModuleFinder(path=[self._project_full_path])
        finder.run_script(file_full_path)

        all_modules = []
        for module in finder.modules.values():
            all_modules.append(self.__get_module_file_name(module))

        all_modules.extend(self._convert_bad_modules_into_paths(base_file_full_path=file_full_path,
                                                                bad_modules=list(finder.badmodules.keys())))

        return [value for value in all_modules if value is not None]

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

        valid_modules.sort(key=lambda valid_module: 0 if not valid_module.layer_index else valid_module.layer_index,
                           reverse=True)
        return valid_modules

    def _set_layer_information(self, hexagonal_module, imported_source):
        if self._project_full_path in imported_source:
            imported_source = imported_source.split(f'{self._project_full_path}/')[1]
        layer_name = imported_source.split('/')[0]
        hexagonal_module.layer_name = layer_name
        hexagonal_module.layer_index = self._composition.get_layer_index_by_module_name(module=layer_name)
