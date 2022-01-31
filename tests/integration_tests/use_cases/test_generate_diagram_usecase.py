import os.path
import sys
import unittest
from tempfile import TemporaryDirectory
from time import sleep
from unittest import TestCase

from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.hexagonal_config import HexagonalConfig
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.use_cases.generate_diagram_usecase import GenerateDiagramUseCase


class TestGenerateDiagramUseCase(TestCase):
    @unittest.skipIf(sys.platform.startswith('win'), 'No Windows Support')
    def test_generate_diagram(self):
        temp_dir = TemporaryDirectory()
        diagram_path = temp_dir.name + '/outputfile'

        hexagonal_config = HexagonalConfig()
        hexagonal_config.add_inner_layer(
            HexagonalLayer(name='infrastructure', directories_groups=[['/infrastructure']]))
        hexagonal_config.add_inner_layer(HexagonalLayer(name='use_cases', directories_groups=[['/usecases']]))
        hexagonal_config.add_inner_layer(HexagonalLayer(name='services', directories_groups=[['/services']]))
        hexagonal_config.add_inner_layer(HexagonalLayer(name='domain', directories_groups=[['/domain']]))

        diagram = GenerateDiagramUseCase()

        self.assertTrue(diagram.execute(project_name='Hexagonal Architecture Diagram',
                                        hexagonal_config=hexagonal_config,
                                        show=False,
                                        output_file_name=diagram_path))
        sleep(0.3)  # Next asserting runs against the disk, I need to wait the file to be confirmed as part of the dir
        self.assertTrue(os.path.isfile(temp_dir.name + '/outputfile.png'))
