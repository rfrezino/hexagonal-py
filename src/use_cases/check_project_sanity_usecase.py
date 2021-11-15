import os
from dataclasses import dataclass
from glob import glob
from modulefinder import ModuleFinder
from typing import List, Optional

from services.hexagonal_composition import HexagonalComposition
from domain.hexagonal_error import HexagonalError
from domain.hexagonal_module import HexagonalModule
from domain.python_file import PythonFile
from services.python_file_builder import PythonFileBuilder


@dataclass
class SanityCheckResponse:
    FilesChecked: List[PythonFile]
    HexagonalErrors: List[HexagonalError]


class CheckProjectSanityUseCase:
    _hexa_modules_dirs_names = List[str]
    _source_folder_full_path: str
    _source_folder: str
    _composition: HexagonalComposition

    def check(self, *, composition: HexagonalComposition, source_folder: str = '') -> List[HexagonalError]:
        self._composition = composition
        self._source_folder_full_path = os.path.abspath(source_folder)
        self._source_folder = self._source_folder_full_path.split('/')[-1]
        self._hexa_modules_dirs_names = self._get_hexa_module_dirs(source_folder=source_folder)

        python_files = self._get_python_file_in_source_folder()

        errors = []
        for python_file in python_files:
            error = self._check_dependencies_order(python_file=python_file)
            if error:
                errors.append(error)

        return errors

    def _get_hexa_module_dirs(self, source_folder: str) -> List[str]:
        source_dir_name = source_folder.split('/')[-1]
        all_dirs = [source_dir_name]
        for layer in self._composition:
            all_dirs += layer.directories

        return all_dirs

    def _get_python_file_in_source_folder(self) -> List[PythonFile]:
        valid_files = []
        python_files = [os.path.abspath(y) for x in os.walk(self._source_folder_full_path)
                        for y in glob(os.path.join(x[0], '*.py'))]
        for python_file in python_files:
            python_file = PythonFileBuilder.build(project_full_path=self._source_folder_full_path,
                                                  file_full_path=python_file,
                                                  composition=self._composition)

            if python_file.layer_index is not None:
                valid_files.append(python_file)

        valid_files.sort(
            key=lambda valid_file: valid_file.layer_index, reverse=True)

        return valid_files

    def _get_modules_used_in_python_file(self, python_file: PythonFile) -> List[HexagonalModule]:
        valid_modules = []
        finder = ModuleFinder(path=[self._source_folder_full_path])
        finder.run_script(python_file.full_path)

        all_modules = list(finder.modules.keys()) + list(finder.badmodules.keys())
        hexa_modules = [module for module in all_modules if
                        any([module.startswith(valid_dir) for valid_dir in self._hexa_modules_dirs_names])]

        for module in hexa_modules:
            hexagonal_module = HexagonalModule(layer_index=None, module=module, layer_name='')

            if self._source_folder in module:
                module = module.split(f'{self._source_folder}.')[1]

            layer_name = module.split('.')[0]
            hexagonal_module.layer_name = layer_name
            hexagonal_module.layer_index = self._composition.get_layer_index_by_module_name(module=layer_name)

            if hexagonal_module.layer_index is None:
                continue

            valid_modules.append(hexagonal_module)

        valid_modules.sort(key=lambda valid_module: valid_module.layer_index, reverse=True)

        return valid_modules

    def _check_dependencies_order(self, python_file: PythonFile) -> Optional[HexagonalError]:
        imported_modules = self._get_modules_used_in_python_file(python_file=python_file)

        for imported_module in imported_modules:
            if python_file.layer_index > imported_module.layer_index:
                return HexagonalError(message='Wrong dependency flow. An inner layer is pointing to an outer layer.',
                                      outer_layer_name=imported_module.layer_name,
                                      inner_layer_name=python_file.module_name,
                                      python_file_problem=python_file.relative_path_from_source_module,
                                      imported_module_problem=imported_module.module)

        return None
