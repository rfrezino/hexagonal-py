from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.hexagonal_config import hexagonal_config

hexagonal_config.add_inner_layer(HexagonalLayer(name='infrastructure', directories_groups=[['/infrastructure']]))
hexagonal_config.add_inner_layer(HexagonalLayer(name='use_cases', directories_groups=[['/usecases']]))
hexagonal_config.add_inner_layer(HexagonalLayer(name='services', directories_groups=[['/services']]))
hexagonal_config.add_inner_layer(HexagonalLayer(name='domain', directories_groups=[['/domain']]))

hexagonal_config.excluded_dirs = ['*/test']