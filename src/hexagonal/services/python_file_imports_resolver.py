import os.path
from modulefinder import ModuleFinder, Module
from typing import List, Optional

from hexagonal.domain.raw_python_file import RawPythonFile


# class PythonProjectHexagonalLayer:
#     _composition: HexagonalComposition
#
#     def _set_layer_information(self, hexagonal_module, imported_source):
#         if self._project_full_path in imported_source:
#             imported_source = imported_source.split(f'{self._project_full_path}/')[1]
#         layer_name = imported_source.split('/')[0]
#         hexagonal_module.layer_name = layer_name
#         hexagonal_module.layer_index = self._composition.get_layer_index_by_module_name(module=layer_name)
#
#     def _get_modules_imported_in_python_file(self, *, file_full_path: str) -> List[PythonModule]:
#         if not os.path.exists(file_full_path):
#             return []
#
#         valid_modules = []
#         all_modules = self._get_all_modules_source_paths(file_full_path=file_full_path)
#
#         imported_sources_from_layers = [module for module in all_modules if
#                                         any([f'/{valid_dir}/' in module for valid_dir in self._used_local_modules])]
#
#         for imported_source in imported_sources_from_layers:
#             hexagonal_module = PythonModule(layer_index=None, module=imported_source, layer_name='')
#             self._set_layer_information(hexagonal_module, imported_source)
#
#             if hexagonal_module.layer_index is not None:
#                 valid_modules.append(hexagonal_module)
#
#         valid_modules.sort(key=lambda valid_module: 0 if not valid_module.layer_index else valid_module.layer_index,
#                            reverse=True)
#         return valid_modules


class PythonFileImportsResolver:
    _raw_python_file: RawPythonFile

    _onion_modules_dirs_names: List[str]
    _used_local_modules: List[str]
    _project_full_path: str

    def resolve_imported_modules(self, *, raw_python_file: RawPythonFile) -> List[str]:
        if not os.path.isfile(raw_python_file.full_path):
            raise Exception(f'Source file not found: {raw_python_file.full_path}')

        self._raw_python_file = raw_python_file

        all_modules = self._get_all_modules_source_paths()

        if raw_python_file.full_path in all_modules:
            all_modules.remove(raw_python_file.full_path)

        return all_modules

    def _get_all_modules_source_paths(self) -> List[str]:
        finder = ModuleFinder(path=[self._raw_python_file.project_folder_full_path])
        finder.run_script(self._raw_python_file.full_path)

        all_modules = []
        for module in finder.modules.values():
            all_modules.append(self.__get_module_file_name(module))

        all_modules.extend(self._convert_bad_modules_into_paths(base_file_full_path=self._raw_python_file.full_path,
                                                                bad_modules=list(finder.badmodules.keys())))

        return [value for value in all_modules if value is not None]

    @staticmethod
    def __get_module_file_name(module: Module) -> Optional[str]:
        string_representation = str(module).strip()
        if not string_representation:
            return None

        try:
            return str(module).split("'")[3]
        except IndexError:
            return None
        except Exception:
            return None

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
