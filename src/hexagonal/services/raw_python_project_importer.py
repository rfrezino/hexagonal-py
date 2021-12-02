import os
from glob import glob
from typing import List

from hexagonal.domain.raw_python_file import RawPythonFile
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.services.raw_python_file_builder import RawPythonFileBuilder


class RawPythonFilesImporter:
    _composition: HexagonalComposition
    _source_folder_full_path: str
    _excluded_folders: List[str]

    @property
    def source_folder_full_path(self):
        return self._source_folder_full_path

    def __init__(self, source_folder_full_path: str, hexagonal_composition: HexagonalComposition,
                 excluded_folders: List[str]):
        if not source_folder_full_path.startswith('/'):
            raise Exception("The param source_folder_full_path must have the source's folder full path.")

        if not os.path.isdir(source_folder_full_path):
            raise Exception('Source folder not found.')

        if not excluded_folders:
            self._excluded_folders = []
        else:
            self._excluded_folders = excluded_folders

        self._source_folder_full_path = source_folder_full_path
        self._composition = hexagonal_composition

    def import_raw_python_files(self) -> List[RawPythonFile]:
        project_files_paths = self._get_all_python_files_paths_from_source_folder()
        python_project_files = self._convert_files_paths_in_python_project_files(python_files_paths=project_files_paths)

        return python_project_files

    def _get_all_python_files_paths_from_source_folder(self) -> List[str]:
        all_files = [os.path.abspath(y) for x in os.walk(self._source_folder_full_path)
                     for y in glob(os.path.join(x[0], '*.py'))]
        result = []
        for file in all_files:
            include_file = True

            if '/.' in file:
                continue

            for excluded_dir in self._excluded_folders:
                file_relative_path = file.replace(self._source_folder_full_path, '')
                if file_relative_path.startswith(excluded_dir):
                    include_file = False
                    break

            if include_file:
                result.append(file)

        return result

    def _convert_files_paths_in_python_project_files(self, python_files_paths: List[str]) -> List[RawPythonFile]:
        result = []
        for python_files_path in python_files_paths:
            result.append(self._convert_file_path_in_python_project_file(python_file_path=python_files_path))

        return result

    def _convert_file_path_in_python_project_file(self, python_file_path: str) -> RawPythonFile:
        builder = RawPythonFileBuilder(file_full_path=python_file_path,
                                       project_source_folder_full_path=self._source_folder_full_path)
        return builder.build()
