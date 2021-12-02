from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.hexagonal_config import hexagonal_config

hexagonal_config.add_inner_layer(HexagonalLayer(name='infrastructure', directories=['/infrastructure']))
hexagonal_config.add_inner_layer(HexagonalLayer(name='use_cases', directories=['/usecases']))
hexagonal_config.add_inner_layer(HexagonalLayer(name='services', directories=['/services']))
hexagonal_config.add_inner_layer(HexagonalLayer(name='domain', directories=['/domain']))

hexagonal_config.excluded_dirs = ['*/test']