from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.main import hexagonal_config

infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['/infrastructure'])
use_cases_layer = HexagonalLayer(name='use_cases', directories=['/use_cases'])
services_layer = HexagonalLayer(name='services', directories=['/services'])
domain_layer = HexagonalLayer(name='domain', directories=['/domain'])

hexagonal_config + infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer
