from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.hexagonal_config import hexagonal_config

hexagonal_config.add_inner_layer(HexagonalLayer(name='adapters', directories_groups=[['/adapters/new_printer'],
                                                                                     ['/adapters/old_printer']]))
hexagonal_config.add_inner_layer(HexagonalLayer(name='port', directories_groups=[['/port']]))
hexagonal_config.add_inner_layer(HexagonalLayer(name='domain', directories_groups=[['/domain']]))

hexagonal_config.excluded_dirs = ['*/test']