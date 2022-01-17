from unittest import TestCase

from hexagonal.services.toml_configuration import TomlConfiguration


class TestTomlConfiguration(TestCase):
    def test_load_from_toml_string_when_input_is_valid_should_parse(self):
        toml_content = """
[tool.hexagonalpy]
excluded_dirs = ['*/test']

[tool.hexagonalpy.layer.1]
name = 'domain'
directories_groups = [['/domain']]

[tool.hexagonalpy.layer.2]
name = 'port'
directories_groups = [['/port']]

[tool.hexagonalpy.layer.3]
name = 'adapters'
directories_groups = [['/adapters/new_printer'], ['/adapters/old_printer']]"""

        toml = TomlConfiguration()

        result = toml.load_from_toml_string(content=toml_content)

        expected_result = {'tool':
                               {'hexagonalpy':
                                    {'excluded_dirs': ['*/test'],
                                     'layer': {'1': {'directories_groups': [['/domain']], 'name': 'domain'},
                                               '2': {'directories_groups': [['/port']], 'name': 'port'},
                                               '3': {'directories_groups': [['/adapters/new_printer'],
                                                                            ['/adapters/old_printer']],
                                                     'name': 'adapters'}}}}}

        self.assertEqual(expected_result, result)
