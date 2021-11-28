import logging
import os
from glob import glob
from typing import List, Optional

from hexagonal.domain.python_file import PythonFile
from hexagonal.domain.python_project import PythonProject
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.services.python_file_builder import PythonFileBuilder


class PythonProjectImporter:
    _composition: HexagonalComposition
    _source_folder_full_path: str

    def import_project(self, *, source_folder: str, composition: HexagonalComposition) -> PythonProject:
        self._composition = composition
        self._source_folder_full_path = os.path.abspath(source_folder)

        python_files = self._import_python_files()

        return PythonProject(full_path=self._source_folder_full_path, python_files=python_files)

    def _get_python_files_in_source_folder(self) -> List[str]:
        return [os.path.abspath(y) for x in os.walk(self._source_folder_full_path)
                for y in glob(os.path.join(x[0], '*.py'))]

    def _import_python_file(self, file: str) -> Optional[PythonFile]:
        logging.info(f'Importing {file}')
        python_file_builder = PythonFileBuilder()
        return python_file_builder.build(project_full_path=self._source_folder_full_path,
                                         file_full_path=file,
                                         composition=self._composition)

    def _import_python_files(self) -> List[PythonFile]:
        valid_files = []
        python_source_files = self._get_python_files_in_source_folder()

        for python_file in python_source_files:
            python_file = self._import_python_file(python_file)
            if python_file.layer_index is None:
                logging.warning(f'File layer index is invalid: {python_file.full_path}')
                continue

            valid_files.append(python_file)

        valid_files.sort(key=lambda valid_file: valid_file.layer_index, reverse=True)
        return valid_files
