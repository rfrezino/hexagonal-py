from unittest import TestCase

from hexagonal.hexagonal_config import HexagonalConfig
from hexagonal.use_cases.check_project_coherence_usecase import CheckProjectCoherenceUseCase
from tests.integration_tests.utils.utils import get_sample_wrong_test_clean_arch_project_path, get_sample_correct_test_clean_arch_project_path


class HexagonalCoherenceCheckUnitTest(TestCase):

    def test_check_when_project_has_wrong_dependencies_import_return_errors(self):
        expected_project_full_path = get_sample_wrong_test_clean_arch_project_path()

        hexagonal_config = HexagonalConfig()
        hexagonal_config.add_inner_layer_with_dirs(layer_name='infrastructure', directories=['/infrastructure'])
        hexagonal_config.add_inner_layer_with_dirs(layer_name='use_cases', directories=['/usecases'])
        hexagonal_config.add_inner_layer_with_dirs(layer_name='services', directories=['/services'])
        hexagonal_config.add_inner_layer_with_dirs(layer_name='domain', directories=['/domain'])

        usecase = CheckProjectCoherenceUseCase(hexagonal_config=hexagonal_config,
                                               source_folder=expected_project_full_path)
        response = usecase.check()

        self.assertEqual(11, len(response.python_files))
        self.assertEqual(len(response.errors), 1)
        error = response.errors[0]
        self.assertEqual(error.message, 'Wrong dependency flow. An inner layer is pointing to an outer layer.')
        self.assertEqual(error.outer_layer_name, 'infrastructure')
        self.assertEqual(error.inner_layer_name, 'use_cases')
        self.assertTrue(error.python_file_problem.endswith('usecases/create_person_usecase.py'))
        self.assertTrue(error.imported_module_problem.endswith('infrastructure/person_mysql_repository.py'))

    def test_check_when_project_has_right_dependencies_import_return_no_errors(self):
        expected_project_full_path = get_sample_correct_test_clean_arch_project_path()

        hexagonal_config = HexagonalConfig()
        hexagonal_config.add_inner_layer_with_dirs(layer_name='infrastructure', directories=['/infrastructure'])
        hexagonal_config.add_inner_layer_with_dirs(layer_name='use_cases', directories=['/usecases'])
        hexagonal_config.add_inner_layer_with_dirs(layer_name='services', directories=['/services'])
        hexagonal_config.add_inner_layer_with_dirs(layer_name='domain', directories=['/domain'])

        usecase = CheckProjectCoherenceUseCase(hexagonal_config=hexagonal_config,
                                               source_folder=expected_project_full_path)
        response = usecase.check()

        self.assertEqual(11, len(response.python_files))
        self.assertEqual(0, len(response.errors))
