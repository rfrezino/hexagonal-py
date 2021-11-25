import os
from glob import glob
from typing import List

from domain.python_file import PythonFile
from domain.python_project import PythonProject
from services.hexagonal_composition import HexagonalComposition
from services.python_file_builder import PythonFileBuilder


class PythonProjectImporter:
    _composition: HexagonalComposition
    _source_folder_full_path: str

    def import_project(self, *, source_folder: str, composition: HexagonalComposition) -> PythonProject:
        self._composition = composition
        self._source_folder_full_path = os.path.abspath(source_folder)

        python_files = self._get_python_file_in_source_folder()

        return PythonProject(full_path=self._source_folder_full_path, python_files=python_files)

    def _get_python_file_in_source_folder(self) -> List[PythonFile]:
        valid_files = []
        python_source_files = [os.path.abspath(y) for x in os.walk(self._source_folder_full_path)
                               for y in glob(os.path.join(x[0], '*.py'))]

        python_file_builder = PythonFileBuilder()
        for python_file in python_source_files:
            python_file = python_file_builder.build(project_full_path=self._source_folder_full_path,
                                                    file_full_path=python_file,
                                                    composition=self._composition)

            if python_file.layer_index is not None:
                valid_files.append(python_file)

        valid_files.sort(key=lambda valid_file: valid_file.layer_index, reverse=True)
        return valid_files
