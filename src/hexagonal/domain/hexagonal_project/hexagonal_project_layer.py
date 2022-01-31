import os
from dataclasses import dataclass
from typing import List, Optional

from hexagonal.domain.python_file import PythonFile


@dataclass
class HexagonalProjectLayer:
    index: int
    name: str
    directories_groups: List[List[str]]
    python_files: List[PythonFile]

    def get_python_file(self, file_full_path: str) -> Optional[PythonFile]:
        for python_file in self.python_files:
            if python_file.file_full_path == file_full_path:
                return python_file
        return None

    def get_directory_group_index_for_file(self, relative_folder_path_from_project_folder: str) -> int:
        if len(self.directories_groups) == 1:
            return 0

        for dir_group_index, dir_group in enumerate(self.directories_groups):
            for dir_name in dir_group:
                if os.path.normcase(os.path.normpath(dir_name)) == relative_folder_path_from_project_folder:
                    return dir_group_index + 1

        return 0

    def is_file_in_layer(self, file_full_path: str) -> bool:
        if self.get_python_file(file_full_path=file_full_path):
            return True
        return False
