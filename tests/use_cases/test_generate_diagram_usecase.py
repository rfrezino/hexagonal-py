from unittest import TestCase

from domain.hexagonal_layer import HexagonalLayer
from services.hexagonal_composition import HexagonalComposition
from use_cases.generate_diagram_usecase import GenerateDiagramUseCase


class TestGenerateDiagramUseCase(TestCase):

    def test_generate_diagram(self):
        infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
        use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
        services_layer = HexagonalLayer(name='services', directories=['services'])
        domain_layer = HexagonalLayer(name='domain', directories=['domain'])

        hexagonal_composition = HexagonalComposition()
        hexagonal_composition + infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer

        diagram = GenerateDiagramUseCase()

        self.assertTrue(diagram.execute(project_name='Hexagonal Architecture Diagram',
                                        hexagonal_composition=hexagonal_composition))
