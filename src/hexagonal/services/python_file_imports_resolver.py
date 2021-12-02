import os.path
from modulefinder import ModuleFinder, Module
from typing import List, Optional

from hexagonal.domain.raw_python_file import RawPythonFile


class PythonFileImportsResolver:
    _raw_python_file: RawPythonFile

    def __init__(self, raw_python_file: RawPythonFile):
        self._raw_python_file = raw_python_file

        if not os.path.isfile(raw_python_file.file_full_path):
            raise Exception(f'Source file not found: {raw_python_file.file_full_path}')

        self._raw_python_file = raw_python_file

    def resolve_imported_modules(self) -> List[str]:
        all_modules = self._get_all_modules_source_paths()

        if self._raw_python_file.file_full_path in all_modules:
            all_modules.remove(self._raw_python_file.file_full_path)

        return all_modules

    def _get_all_modules_source_paths(self) -> List[str]:
        # finder = ModuleFinder(path=[self._raw_python_file.project_folder_full_path])
        finder = ModuleFinder(path=[])
        finder.run_script(self._raw_python_file.file_full_path)

        all_modules = []
        for module in finder.modules.values():
            all_modules.append(self.__get_module_file_name(module))

        all_modules.extend(
            self._convert_bad_modules_into_paths(base_file_full_path=self._raw_python_file.file_full_path,
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

    def _convert_bad_modules_into_paths(self, base_file_full_path: str, bad_modules: List[str]) -> List[str]:
        result = []

        for bad_module in bad_modules:
            bad_module_file = bad_module.replace('.', '/') + '.py'

            while '/' in bad_module_file:
                full_bad_module_file = self._raw_python_file.project_folder_full_path + '/' + bad_module_file

                if os.path.isfile(full_bad_module_file):
                    result.append(full_bad_module_file)
                    break

                bad_module_file = bad_module_file.split('/', 1)[1]

        return result
