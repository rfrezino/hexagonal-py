from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.hexagonal_config import hexagonal_config

hexagonal_config.add_inner_layer_with_dirs(layer_name='infrastructure', directories=['/infrastructure'])
hexagonal_config.add_inner_layer_with_dirs(layer_name='use_cases', directories=['/use_cases'])
hexagonal_config.add_inner_layer_with_dirs(layer_name='services', directories=['/services'])
hexagonal_config.add_inner_layer_with_dirs(layer_name='domain', directories=['/domain'])
