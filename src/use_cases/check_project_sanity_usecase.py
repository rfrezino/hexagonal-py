from dataclasses import dataclass
from typing import List, Optional

from domain.hexagonal_check_response import HexagonalCheckResponse
from domain.hexagonal_error import HexagonalError
from domain.python_file import PythonFile
from services.hexagonal_composition import HexagonalComposition
from services.python_project_importer import PythonProjectImporter


@dataclass
class SanityCheckResponse:
    FilesChecked: List[PythonFile]
    HexagonalErrors: List[HexagonalError]


class CheckProjectSanityUseCase:
    _hexa_modules_dirs_names = List[str]
    _source_folder_full_path: str
    _source_folder: str
    _composition: HexagonalComposition

    def check(self, *, composition: HexagonalComposition, source_folder: str = '') -> HexagonalCheckResponse:
        importer = PythonProjectImporter()
        python_project = importer.import_project(source_folder=source_folder, composition=composition)

        errors = []
        for python_file in python_project.python_files:
            error = self._check_dependencies_order(python_file=python_file)
            if error:
                errors.append(error)

        result = HexagonalCheckResponse()
        result.errors = errors
        result.project = python_project

        return result

    @staticmethod
    def _check_dependencies_order(python_file: PythonFile) -> Optional[HexagonalError]:
        for imported_module in python_file.imported_modules:
            if python_file.layer_index > imported_module.layer_index:
                return HexagonalError(message='Wrong dependency flow. An inner layer is pointing to an outer layer.',
                                      outer_layer_name=imported_module.layer_name,
                                      inner_layer_name=python_file.layer_name,
                                      python_file_problem=python_file.relative_path_from_source_module,
                                      imported_module_problem=imported_module.module)

        return None
