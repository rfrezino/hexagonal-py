import os
from dataclasses import dataclass
from typing import List, Optional

from hexagonal.domain.hexagonal_check_response import HexagonalCheckResponse
from hexagonal.domain.hexagonal_error import HexagonalError
from hexagonal.domain.python_file import PythonFile
from hexagonal.domain.raw_python_file import RawPythonFile
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.services.python_file_builder import PythonFileBuilder
from hexagonal.services.raw_python_project_importer import RawPythonFilesImporter


@dataclass
class SanityCheckResponse:
    FilesChecked: List[RawPythonFile]
    HexagonalErrors: List[HexagonalError]


class CheckProjectSanityUseCase:
    _hexa_modules_dirs_names = List[str]
    _source_folder_full_path: str
    _source_folder: str
    _composition: HexagonalComposition

    def __init__(self, composition: HexagonalComposition, source_folder: str = ''):
        self._source_folder = os.path.abspath(source_folder)
        self._composition = composition

    def check(self) -> HexagonalCheckResponse:
        python_files = self._get_python_files_from_project()

        errors = []
        for python_file in python_files:
            error = self._check_dependencies_order(python_file=python_file)
            if error:
                errors.append(error)

        result = HexagonalCheckResponse()
        result.errors = errors
        result.python_files = python_files
        return result

    def _get_python_files_from_project(self) -> List[PythonFile]:
        importer = RawPythonFilesImporter(source_folder_full_path=self._source_folder,
                                          hexagonal_composition=self._composition)
        raw_python_files = importer.import_raw_python_files()
        return self._convert_raw_python_files_into_python_files(raw_python_files=raw_python_files)

    @staticmethod
    def _convert_raw_python_files_into_python_files(raw_python_files: List[RawPythonFile]) -> List[PythonFile]:
        result = []
        python_file_builder = PythonFileBuilder()
        for raw_python_file in raw_python_files:
            result.append(python_file_builder.build(raw_python_file=raw_python_file))

        return result

    @staticmethod
    def _check_dependencies_order(python_file: PythonFile) -> Optional[HexagonalError]:
        for imported_module in python_file.imported_modules:
            if python_file.layer_index is None or imported_module.layer_index is None:
                continue

            if python_file.layer_index > imported_module.layer_index:
                return HexagonalError(message='Wrong dependency flow. An inner layer is pointing to an outer layer.',
                                      outer_layer_name=imported_module.layer_name,
                                      inner_layer_name=python_file.layer_name,
                                      python_file_problem=python_file.relative_path_from_source_module,
                                      imported_module_problem=imported_module.module)

        return None
