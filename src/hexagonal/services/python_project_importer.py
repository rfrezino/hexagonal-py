import logging
import os
from glob import glob
from typing import List

from hexagonal.domain.python_file import PythonFile
from hexagonal.domain.python_project import PythonProject
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.services.python_file_builder import PythonFileBuilder


class PythonProjectImporter:
    _composition: HexagonalComposition
    _source_folder_full_path: str

    @property
    def source_folder_full_path(self):
        return self._source_folder_full_path

    def __init__(self, source_folder_full_path: str, hexagonal_composition: HexagonalComposition):
        if not source_folder_full_path.startswith('/'):
            raise Exception("The param source_folder_full_path must have the source's folder full path.")

        if not os.path.isdir(source_folder_full_path):
            raise Exception('Source folder not found.')

        self._source_folder_full_path = source_folder_full_path
        self._composition = hexagonal_composition

    def import_project(self) -> PythonProject:
        project_files_paths = self._get_all_python_files_paths_from_source_folder()
        python_project_files = self._convert_files_paths_in_python_project_files(python_files_paths=project_files_paths)

        python_files = self._import_python_files()

        return PythonProject(full_path=self._source_folder_full_path, python_files=python_files)

    def _get_all_python_files_paths_from_source_folder(self) -> List[str]:
        return [os.path.abspath(y) for x in os.walk(self._source_folder_full_path)
                for y in glob(os.path.join(x[0], '*.py'))]

    def _convert_files_paths_in_python_project_files(self, python_files_paths: List[str]) -> List[PythonFile]:
        result = []
        for python_files_path in python_files_paths:
            result += self._convert_file_path_in_python_project_file(python_file_path=python_files_path)

        return result

    def _convert_file_path_in_python_project_file(self, python_file_path: str) -> PythonFile:
        builder = PythonFileBuilder(file_full_path=python_file_path)
        return builder.build()


    def _get_python_files_in_source_folder(self) -> List[str]:
        return [os.path.abspath(y) for x in os.walk(self._source_folder_full_path)
                for y in glob(os.path.join(x[0], '*.py'))]

    def _import_python_file(self, file: str) -> PythonFile:
        logging.info(f'Importing {file}')
        python_file_builder = PythonFileBuilder()
        return python_file_builder.build(project_full_path=self._source_folder_full_path,
                                         file_full_path=file,
                                         composition=self._composition)

    def _import_python_files(self) -> List[PythonFile]:
        valid_files: List[PythonFile] = []
        python_source_files = self._get_python_files_in_source_folder()

        for python_file in python_source_files:
            imported_python_file = self._import_python_file(python_file)
            if imported_python_file.layer_index is None:
                logging.warning(f'File layer index is invalid: {imported_python_file.full_path}')
                continue

            valid_files.append(imported_python_file)

        valid_files.sort(key=lambda valid_file: 0 if valid_file.layer_index is None else valid_file.layer_index,
                         reverse=True)
        return valid_files
