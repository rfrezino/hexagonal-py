import os.path
from typing import List
from unittest import TestCase

from hexagonal.domain.raw_python_file import RawPythonFile
from hexagonal.services.python_file_imports_resolver import PythonFileImportsResolver
from tests.integration_tests.utils.utils import get_sample_correct_test_clean_arch_project_path


class TestPythonFileImportsResolver(TestCase):
    @staticmethod
    def assertContainsItemWithSuffix(expected_suffix: str, item_list: List[str]):
        if not any(item.endswith(expected_suffix) for item in item_list):
            raise Exception(f'Item with suffix {expected_suffix} not found in {item_list}')

    def test_resolve_imported_modules_when_file_is_valid_return_list_of_imported_modules(self):
        project_path = get_sample_correct_test_clean_arch_project_path()
        file_path = os.path.normcase(os.path.normpath(project_path + '/usecases/create_person_usecase.py'))

        raw_python_file = RawPythonFile(
            file_full_path=file_path,
            file_name='create_person_usecase.py',
            file_folder_full_path=os.path.normpath(project_path + '/usecases'),
            relative_folder_path_from_project_folder=os.path.normpath('/usecases'),
            project_folder_full_path=project_path,
        )

        imports_resolver = PythonFileImportsResolver(raw_python_file=raw_python_file)
        imported_modules = imports_resolver.resolve_imported_modules()

        self.assertEqual(len(imported_modules), 2, imported_modules)
        self.assertContainsItemWithSuffix('person.py', imported_modules)
        self.assertContainsItemWithSuffix('person_repository.py', imported_modules)
