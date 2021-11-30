import os
from unittest import TestCase

from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.services.python_project_importer import PythonProjectImporter


class TestPythonProjectImporter(TestCase):
    def test_init_should_raise_exception_when_params_source_folder_full_path_is_relative_path(self):
        invalid_source_path = '~/test'

        with self.assertRaises(Exception) as error:
            importer = PythonProjectImporter(source_folder_full_path=invalid_source_path,
                                             hexagonal_composition=HexagonalComposition())
        self.assertEqual("The param source_folder_full_path must have the source's folder full path.",
                         str(error.exception))

    def test_init_should_raise_exception_when_params_source_folder_full_path_does_not_exits(self):
        invalid_source_path = '/nonexist'

        with self.assertRaises(Exception) as error:
            importer = PythonProjectImporter(source_folder_full_path=invalid_source_path,
                                             hexagonal_composition=HexagonalComposition())

        self.assertEqual('Source folder not found.', str(error.exception))

    def test_init_should_return_valid_object_when_params_are_correct(self):
        valid_source_path = os.path.abspath('./')

        importer = PythonProjectImporter(source_folder_full_path=valid_source_path,
                                         hexagonal_composition=HexagonalComposition())

        self.assertEqual(valid_source_path, importer.source_folder_full_path)
