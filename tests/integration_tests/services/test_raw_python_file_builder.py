import os
from unittest import TestCase

from hexagonal.services.raw_python_file_builder import RawPythonFileBuilder
from tests.utils import fix_path


class TestRawPythonFileBuilder(TestCase):

    def test_init_should_return_valid_object_when_params_are_correct(self):
        valid_source_path = fix_path(os.path.abspath(__file__))
        file_folder = fix_path(os.path.abspath(__file__.replace('test_raw_python_file_builder.py', '')))

        builder = RawPythonFileBuilder(file_full_path=valid_source_path, project_source_folder_full_path=file_folder)

        self.assertEqual(valid_source_path, builder.file_full_path)

    def test_init_should_raise_exception_when_file_and_project_paths_does_not_match(self):
        with self.assertRaises(Exception) as error:
            builder = RawPythonFileBuilder(file_full_path='/path/a/file.py',
                                           project_source_folder_full_path='/path/b')

        self.assertEqual('File path and project path do not match.', str(error.exception))

    def test_build_should_return_valid_object_when_params_are_correct(self):
        valid_source_path = fix_path(os.path.abspath(__file__))
        file_folder = fix_path(os.path.abspath(__file__.replace('test_raw_python_file_builder.py', '')))
        project_folder = file_folder.split(f'{os.sep}services')[0]

        builder = RawPythonFileBuilder(file_full_path=valid_source_path, project_source_folder_full_path=project_folder)
        raw_python_file = builder.build()

        self.assertEqual(valid_source_path, raw_python_file.file_full_path)
        self.assertEqual('test_raw_python_file_builder.py', raw_python_file.file_name)
        self.assertEqual(file_folder, raw_python_file.file_folder_full_path)
        self.assertEqual(f'{os.sep}services', raw_python_file.relative_folder_path_from_project_folder)
