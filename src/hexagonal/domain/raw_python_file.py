from dataclasses import dataclass


@dataclass
class RawPythonFile:
    file_full_path: str
    file_name: str
    file_folder_full_path: str
    # For instance if the project is located at: /usr/project/
    # and the file is /usr/project/services/another/file.py
    # the project_relative_folder_path is "services/another"
    relative_folder_path_from_project_folder: str
    project_folder_full_path: str

