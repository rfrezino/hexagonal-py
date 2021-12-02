from hexagonal.domain.python_file import PythonFile
from hexagonal.domain.raw_python_file import RawPythonFile
from hexagonal.services.python_file_imports_resolver import PythonFileImportsResolver


class PythonFileBuilder:

    @staticmethod
    def build(raw_python_file: RawPythonFile) -> PythonFile:
        imports_resolver = PythonFileImportsResolver()
        imported_modules = imports_resolver.resolve_imported_modules(raw_python_file=raw_python_file)

        return PythonFile(
            file_full_path=raw_python_file.file_full_path,
            file_name=raw_python_file.file_name,
            file_folder_full_path=raw_python_file.file_folder_full_path,
            relative_folder_path_from_project_folder=raw_python_file.relative_folder_path_from_project_folder,
            project_folder_full_path=raw_python_file.project_folder_full_path,
            imported_modules=imported_modules)
