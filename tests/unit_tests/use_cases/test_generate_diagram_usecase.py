import os.path
from tempfile import TemporaryDirectory
from time import sleep
from unittest import TestCase

from domain.hexagonal_layer import HexagonalLayer
from services.hexagonal_composition import HexagonalComposition
from use_cases.generate_diagram_usecase import GenerateDiagramUseCase


class TestGenerateDiagramUseCase(TestCase):
    def test_generate_diagram(self):
        temp_dir = TemporaryDirectory()
        diagram_path = temp_dir.name + '/outputfile'

        infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
        use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
        services_layer = HexagonalLayer(name='services', directories=['services'])
        domain_layer = HexagonalLayer(name='domain', directories=['domain'])

        hexagonal_composition = HexagonalComposition()
        hexagonal_composition + infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer

        diagram = GenerateDiagramUseCase()

        self.assertTrue(diagram.execute(project_name='Hexagonal Architecture Diagram',
                                        hexagonal_composition=hexagonal_composition,
                                        show=False,
                                        output_file_name=diagram_path))
        sleep(0.3)  # Next asserting runs agains the disk so I need to wait the file to be confirmed as part of the dir
        self.assertTrue(os.path.isfile(temp_dir.name + '/outputfile.png'))