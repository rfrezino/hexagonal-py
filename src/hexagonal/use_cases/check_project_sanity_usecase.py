import os
from typing import List

from hexagonal.domain.hexagonal_error import HexagonalError
from hexagonal.domain.hexagonal_project.hexagonal_project import HexagonalProject
from hexagonal.domain.python_file import PythonFile
from hexagonal.domain.raw_python_file import RawPythonFile
from hexagonal.hexagonal_config import HexagonalConfig
from hexagonal.services.hexagonal_dependency_flow_checker import HexagonalDependencyFlowChecker, DependencyFlowError
from hexagonal.services.hexagonal_project_builder import HexagonalProjectBuilder
from hexagonal.services.python_file_builder import PythonFileBuilder
from hexagonal.services.raw_python_project_importer import RawPythonFilesImporter


class HexagonalCheckResponse:
    errors: List[HexagonalError]
    python_files: List[PythonFile]
    hexagonal_project: HexagonalProject


class CheckProjectSanityUseCase:
    _source_folder_full_path: str
    _source_folder: str
    _hexagonal_config: HexagonalConfig

    def __init__(self, *, hexagonal_config: HexagonalConfig, source_folder: str = ''):
        self._source_folder = os.path.abspath(source_folder)
        self._hexagonal_config = hexagonal_config

    def check(self) -> HexagonalCheckResponse:
        python_files = self._get_python_files_from_project()
        hexagonal_project_builder = HexagonalProjectBuilder(
            python_files=python_files,
            hexagonal_composition=self._hexagonal_config.layers)
        hexagonal_project = hexagonal_project_builder.build()

        flow_checker = HexagonalDependencyFlowChecker(hexagonal_project=hexagonal_project)
        flow_checker_response = flow_checker.check()

        result = HexagonalCheckResponse()
        result.errors = self._convert_flow_errors(flow_checker_response.errors)
        result.python_files = python_files
        result.hexagonal_project = hexagonal_project
        return result

    def _get_python_files_from_project(self) -> List[PythonFile]:
        importer = RawPythonFilesImporter(source_folder_full_path=self._source_folder,
                                          hexagonal_composition=self._hexagonal_config.layers,
                                          excluded_folders=self._hexagonal_config.excluded_dirs)
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
    def _convert_flow_errors(errors: List[DependencyFlowError]) -> List[HexagonalError]:
        result = []
        for error in errors:
            new_error = HexagonalError(message='Wrong dependency flow. An inner layer is pointing to an outer layer.',
                                       outer_layer_name=error.imported_module_layer.name,
                                       inner_layer_name=error.source_file_layer.name,
                                       python_file_problem=error.source_file.file_full_path,
                                       imported_module_problem=error.imported_module.file_full_path)
            result.append(new_error)

        return result
