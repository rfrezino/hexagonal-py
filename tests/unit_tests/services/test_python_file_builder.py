from unittest import TestCase

from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.services.python_file_builder import PythonFileBuilder


class TestPythonFileBuilder(TestCase):
    def test_build_when_params_correct_return_valid_object(self):
        # Setup
        layer_use_case = HexagonalLayer('Use cases', ['use_cases'])
        project_full_path = '/Users/dev/project_check/correct_project'
        file_full_path = project_full_path + '/use_cases/add_usecase.py'

        composition = HexagonalComposition()
        composition + layer_use_case

        # Execute
        builder = PythonFileBuilder()
        python_file = builder.build(
            project_full_path=project_full_path,
            file_full_path=file_full_path,
            composition=composition
        )

        # Assert
        self.assertEqual(python_file.full_path, file_full_path, 'Wrong path')
        self.assertEqual(python_file.relative_path_from_source_module, 'use_cases/add_usecase.py',
                         'Wrong relative path')
        self.assertEqual(python_file.layer_name, 'use_cases', 'Wrong layer name')
        self.assertEqual(python_file.layer_index, 1, 'Wrong layer number')
