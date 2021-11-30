from unittest import TestCase

from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.use_cases.check_project_sanity_usecase import CheckProjectSanityUseCase
from tests.utils import get_sample_wrong_test_project_path, get_sample_correct_test_project_path


class HexagonalSanityCheckUnitTest(TestCase):

    def test_check_when_project_has_wrong_dependencies_import_return_errors(self):
        expected_project_full_path = get_sample_wrong_test_project_path()

        infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
        use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
        services_layer = HexagonalLayer(name='services', directories=['services'])
        domain_layer = HexagonalLayer(name='domain', directories=['domain'])

        hexagonal_composition = HexagonalComposition()
        hexagonal_composition + infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer

        usecase = CheckProjectSanityUseCase()
        response = usecase.check(composition=hexagonal_composition,
                                 source_folder=expected_project_full_path)

        self.assertEqual(len(response.project.python_files), 8)
        self.assertEqual(response.project.full_path, expected_project_full_path)
        self.assertEqual(len(response.errors), 1)
        self.assertEqual(response.errors[0].message,
                         'Wrong dependency flow. An inner layer is pointing to an outer layer.')
        self.assertEqual(response.errors[0].outer_layer_name, 'infrastructure')
        self.assertEqual(response.errors[0].inner_layer_name, 'usecases')
        self.assertEqual(response.errors[0].python_file_problem, 'usecases/create_person_usecase.py')
        self.assertTrue(response.errors[0].imported_module_problem.endswith(
            'test_projects/wrong_project/infrastructure/person_mysql_repository.py'))

    def test_check_when_project_has_right_dependencies_import_return_no_errors(self):
        expected_project_full_path = get_sample_correct_test_project_path()

        infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
        use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
        services_layer = HexagonalLayer(name='services', directories=['services'])
        domain_layer = HexagonalLayer(name='domain', directories=['domain'])

        hexagonal_composition = HexagonalComposition()
        hexagonal_composition + infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer

        usecase = CheckProjectSanityUseCase()
        response = usecase.check(composition=hexagonal_composition, source_folder=expected_project_full_path)

        self.assertEqual(len(response.project.python_files), 8)
        self.assertEqual(response.project.full_path, expected_project_full_path)
        self.assertEqual(len(response.errors), 0)
