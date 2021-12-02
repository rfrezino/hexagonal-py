import os.path

from hexagonal.domain.raw_python_file import RawPythonFile


class RawPythonFileBuilder:
    _file_full_path: str
    _file_name: str
    _file_folder: str
    _project_source_folder_full_path: str

    @property
    def file_full_path(self) -> str:
        return self._file_full_path

    def __init__(self, file_full_path: str, project_source_folder_full_path: str):
        if not file_full_path.startswith(project_source_folder_full_path):
            raise Exception('File path and project path do not match.')

        if not file_full_path.startswith('/'):
            raise Exception("The param file_full_path must have the file's full path.")

        if not file_full_path.endswith('.py'):
            raise Exception('File must have .py extension.')

        self._file_full_path = file_full_path
        self._project_source_folder_full_path = os.path.abspath(project_source_folder_full_path)

    def _get_file_name_from_full_file_path(self) -> str:
        return self._file_full_path.split('/')[-1]

    def _get_file_folder_path(self) -> str:
        return os.path.abspath(self.file_full_path.replace(self._file_name, ''))

    def _get_relative_folder_path_from_project_folder(self) -> str:
        folder_relative_path = self.file_full_path.replace(self._project_source_folder_full_path, '')
        folder_relative_path = folder_relative_path.replace(self._file_name, '')
        return folder_relative_path[0:-1]

    def build(self) -> RawPythonFile:
        self._file_name = self._get_file_name_from_full_file_path()
        self._file_folder = self._get_file_folder_path()
        return RawPythonFile(
            file_full_path=self._file_full_path,
            file_name=self._file_name,
            file_folder_full_path=self._file_folder,
            relative_folder_path_from_project_folder=self._get_relative_folder_path_from_project_folder(),
            project_folder_full_path=self._project_source_folder_full_path)
