from unittest import TestCase

from hexagonal.services.toml_configuration import TomlConfiguration


class TestTomlConfiguration(TestCase):
    _valid_toml_configuration = """
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

    def test_load_from_toml_string_should_parse_when_input_valid(self):
        toml = TomlConfiguration()

        result = toml.load_from_string(content=self._valid_toml_configuration)

        expected_result = {'tool':
                               {'hexagonalpy':
                                    {'excluded_dirs': ['*/test'],
                                     'layer': {'1': {'directories_groups': [['/domain']], 'name': 'domain'},
                                               '2': {'directories_groups': [['/port']], 'name': 'port'},
                                               '3': {'directories_groups': [['/adapters/new_printer'],
                                                                            ['/adapters/old_printer']],
                                                     'name': 'adapters'}}}}}

        self.assertEqual(expected_result, result)

    def test_has_hexagonalpy_configuration_return_true_when_configuration_exists(self):
        toml = TomlConfiguration()
        result = toml.load_from_string(content=self._valid_toml_configuration)
        toml.has_hexagonalpy_configuration()
        self.assertTrue(result)

    def test_has_hexagonalpy_configuration_return_false_when_configuration_doesnt_exist(self):
        toml = TomlConfiguration()
        toml.load_from_string(content='')
        result = toml.has_hexagonalpy_configuration()

        self.assertFalse(result)
