from os import error
from unittest import TestCase
import unittest

from src.hexa_commands import run_command
from src.hexa_layer import HexagonalLayer
from src.hexa_sanity_check import HexagonalSanityCheck


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
        self.assertEqual(len(errors), 0)

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
