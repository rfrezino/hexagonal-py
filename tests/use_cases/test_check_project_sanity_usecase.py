from unittest import TestCase

from domain.hexagonal_error import HexagonalError
from domain.hexagonal_layer import HexagonalLayer
from services.hexagonal_composition import HexagonalComposition
from use_cases.check_project_sanity_usecase import CheckProjectSanityUseCase


class HexagonalSanityCheckUnitTest(TestCase):
    def test_check_when_project_has_wrong_dependencies_import_return_errors(self):
        infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
        use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
        services_layer = HexagonalLayer(name='services', directories=['services'])
        domain_layer = HexagonalLayer(name='domain', directories=['domain'])

        hexagonal_composition = HexagonalComposition()
        hexagonal_composition + infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer

        usecase = CheckProjectSanityUseCase()
        errors = usecase.check(composition=hexagonal_composition, source_folder='./test_projects/wrong_project/')
        self.assertEqual(errors,
                         [HexagonalError(message='Wrong dependency flow. An inner layer is pointing to an outer layer.',
                                         outer_layer_name='infrastructure',
                                         inner_layer_name='usecases',
                                         python_file_problem='usecases/create_person_usecase.py',
                                         imported_module_problem='tests.use_cases.test_projects.wrong_project.infrastructure.person_mysql_repository')])

    def test_check_when_project_has_right_dependencies_import_return_no_errors(self):
        infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
        use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
        services_layer = HexagonalLayer(name='services', directories=['services'])
        domain_layer = HexagonalLayer(name='domain', directories=['domain'])

        hexagonal_composition = HexagonalComposition()
        hexagonal_composition + infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer

        usecase = CheckProjectSanityUseCase()
        errors = usecase.check(composition=hexagonal_composition, source_folder='./test_projects/correct_project/')
        self.assertEqual(len(errors), 0)
