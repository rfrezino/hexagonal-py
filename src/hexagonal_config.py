from cli import hexagonal_composition
from domain.hexagonal_layer import HexagonalLayer

infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
services_layer = HexagonalLayer(name='services', directories=['services'])
domain_layer = HexagonalLayer(name='domain', directories=['domain'])

hexagonal_composition + infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer
