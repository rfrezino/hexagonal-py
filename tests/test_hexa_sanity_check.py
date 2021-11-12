from os import error
from unittest import TestCase
import unittest

from src.hexa_commands import run_command
from src.hexa_layer import HexagonalLayer
from src.hexa_sanity_check import HexagonalError, HexagonalSanityCheck


class HexagonalSanityCheckUnitTest(TestCase):
    def test_check_when_project_has_wrong_dependencies_import_return_errors(self):
        # Project Onion Architecture Structure
        infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
        use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
        services_layer = HexagonalLayer(name='services', directories=['services'])
        domain_layer = HexagonalLayer(name='domain', directories=['domain'])

        infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer

        checker = HexagonalSanityCheck()
        errors = checker.check('./tests/test_projects/wrong_project/')
        self.assertEqual(errors, 
                         [HexagonalError(message='Wrong dependency flow. An inner layer is pointing to an outer layer.', 
                                         outer_layer_name='infrastructure', 
                                         inner_layer_name='usecases', 
                                         python_file_problem='usecases/create_person_usecase.py', 
                                         imported_module_problem='tests.test_projects.wrong_project.infrastructure.person_mysql_repository')])
        

        

    def test_check_when_project_has_right_dependencies_import_return_no_errors(self):
        # Project Onion Architecture Structure
        infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
        use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
        services_layer = HexagonalLayer(name='services', directories=['services'])
        domain_layer = HexagonalLayer(name='domain', directories=['domain'])

        infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer

        checker = HexagonalSanityCheck()
        errors = checker.check('src/')
        self.assertEqual(len(errors), 0)


if __name__ == '__main__':
    unittest.main()
