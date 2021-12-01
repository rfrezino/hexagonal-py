import os
from asyncio import sleep
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase

from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.services.python_file_builder import PythonFileBuilder


class TestPythonFileBuilder(TestCase):

    def test_init_should_raise_exception_when_param_file_full_path_is_relative_path(self):
        invalid_source_path = '~/test.py'

        with self.assertRaises(Exception) as error:
            builder = PythonFileBuilder(file_full_path=invalid_source_path)
        self.assertEqual("The param file_full_path must have the file's full path.", str(error.exception))

    def test_init_should_raise_exception_when_param_file_full_path_does_not_exits(self):
        invalid_source_path = '/nonexist.py'

        with self.assertRaises(Exception) as error:
            builder = PythonFileBuilder(file_full_path=invalid_source_path)

        self.assertEqual('Source file not found.', str(error.exception))

    def test_init_should_return_valid_object_when_params_are_correct(self):
        valid_source_path = os.path.abspath(__file__)
        file_folder = os.path.abspath(__file__.replace('test_python_file_builder.py', ''))

        builder = PythonFileBuilder(file_full_path=valid_source_path)

        self.assertEqual(valid_source_path, builder.file_full_path)
        self.assertEqual('test_python_file_builder.py', builder.file_name)
        self.assertEqual(file_folder, builder.file_folder)

    # def test_build_when_params_correct_return_valid_object(self):
    #     # Setup
    #     layer_use_case = HexagonalLayer('Use cases', ['use_cases'])
    #     project_full_path = '/Users/dev/project_check/correct_project'
    #     file_full_path = project_full_path + '/use_cases/add_usecase.py'
    #
    #     composition = HexagonalComposition()
    #     composition + layer_use_case
    #
    #     # Execute
    #     builder = PythonFileBuilder(file_full_path=file_full_path)
    #     python_file = builder.build(
    #         project_full_path=project_full_path,
    #         composition=composition
    #     )
    #
    #     # Assert
    #     self.assertEqual(python_file.full_path, file_full_path, 'Wrong path')
    #     self.assertEqual(python_file.relative_path_from_source_module, 'use_cases/add_usecase.py',
    #                      'Wrong relative path')
    #     self.assertEqual(python_file.layer_name, 'use_cases', 'Wrong layer name')
    #     self.assertEqual(python_file.layer_index, 1, 'Wrong layer number')
    #
    # def test_build_when_params_nested_folders_return_valid_object(self):
    #     # Setup
    #     layer_use_case = HexagonalLayer('Use cases', ['something_else/use_cases'])
    #     project_full_path = '/Users/dev/project_check/correct_project'
    #     file_full_path = project_full_path + '/something_else/use_cases/add_usecase.py'
    #
    #     composition = HexagonalComposition()
    #     composition + layer_use_case
    #
    #     # Execute
    #     builder = PythonFileBuilder(file_full_path=file_full_path)
    #     python_file = builder.build(
    #         project_full_path=project_full_path,
    #         composition=composition
    #     )
    #
    #     # Assert
    #     self.assertEqual(python_file.full_path, file_full_path, 'Wrong path')
    #     self.assertEqual(python_file.relative_path_from_source_module, 'something_else/use_cases/add_usecase.py',
    #                      'Wrong relative path')
    #     self.assertEqual(python_file.layer_name, 'something_else/use_cases', 'Wrong layer name')
    #     self.assertEqual(python_file.layer_index, 1, 'Wrong layer number')
