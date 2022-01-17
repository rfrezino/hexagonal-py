from typing import MutableMapping, Any

import toml


class TomlConfigurationException(Exception):
    pass


class TomlConfiguration:
    _configuration: MutableMapping[str, Any]

    def load_from_file(self, file_path: str):
        pass

    def load_from_toml_string(self, *, content: str) -> MutableMapping[str, Any]:
        self._configuration = toml.loads(content)
        return self._configuration

    def has_hexagonalpy_configuration(self) -> bool:
        try:
            self._configuration['tool']['hexagonalpy']
        except KeyError:
            return False

        return True