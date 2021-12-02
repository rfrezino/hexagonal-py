import os
from unittest import TestCase

from hexagonal.domain.raw_python_file import RawPythonFile
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.services.raw_python_project_importer import RawPythonFilesImporter
from tests.integration_tests.utils.utils import get_sample_correct_test_project_path


class TestPythonProjectImporter(TestCase):
    def test_init_should_raise_exception_when_params_source_folder_full_path_is_relative_path(self):
        invalid_source_path = '~/test'

        with self.assertRaises(Exception) as error:
            importer = RawPythonFilesImporter(source_folder_full_path=invalid_source_path,
                                              hexagonal_composition=HexagonalComposition())
        self.assertEqual("The param source_folder_full_path must have the source's folder full path.",
                         str(error.exception))

    def test_init_should_raise_exception_when_params_source_folder_full_path_does_not_exits(self):
        invalid_source_path = '/nonexist'

        with self.assertRaises(Exception) as error:
            importer = RawPythonFilesImporter(source_folder_full_path=invalid_source_path,
                                              hexagonal_composition=HexagonalComposition())

        self.assertEqual('Source folder not found.', str(error.exception))

    def test_init_should_return_valid_object_when_params_are_correct(self):
        valid_source_path = os.path.abspath('/')

        importer = RawPythonFilesImporter(source_folder_full_path=valid_source_path,
                                          hexagonal_composition=HexagonalComposition())

        self.assertEqual(valid_source_path, importer.source_folder_full_path)

    def test_import_project_when_project_exits_return_imported_project(self):
        expected = RawPythonProject(
            full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project',
            python_files=[RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/__init__.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/main.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/hexagonal_config.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/infrastructure/person_mysql_repository.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/infrastructure/__init__.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/domain/person.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/domain/__init__.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/usecases/create_person_usecase.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/usecases/__init__.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/services/__init__.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[]), RawPythonFile(
                full_path='/Users/rodrigo.rezino/Private/hexagonal-sanity-check/tests/integration_tests/utils/sample_projects/correct_project/services/person_repository.py',
                relative_path_from_source_module='', layer_name='', layer_index=0, imported_modules=[])])
        importer = RawPythonFilesImporter(source_folder_full_path=get_sample_correct_test_project_path(),
                                          hexagonal_composition=HexagonalComposition())
        response = importer.import_raw_python_files()

        self.assertEqual(expected, response)
