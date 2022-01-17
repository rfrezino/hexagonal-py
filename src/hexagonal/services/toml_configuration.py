from typing import MutableMapping, Any, List

import toml


class TomlConfigurationException(Exception):
    pass


class TomlConfiguration:
    _configuration: MutableMapping[str, Any]

    def load_from_file(self, file_path: str):
        with open(file_path) as f:
            content = f.read()
            self.load_from_string(content=content)

    def load_from_string(self, *, content: str) -> MutableMapping[str, Any]:
        self._configuration = toml.loads(content)
        return self._configuration

    def has_hexagonalpy_configuration(self) -> bool:
        try:
            self._configuration['tool']['hexagonalpy']
        except KeyError:
            return False

        return True

    def excluded_dirs(self) -> List[str]:
        try:
            return self._configuration['tool']['hexagonalpy']['excluded_dirs']
        except KeyError:
            return []

    def layers(self) -> List[Any]:
        try:
            result = []
            sorted_keys = list(self._configuration['tool']['hexagonalpy']['layer'].keys())
            sorted_keys.sort(reverse=True)

            for key in sorted_keys:
                result.append(self._configuration['tool']['hexagonalpy']['layer'][f'{key}'])

            return result
        except KeyError:
            return []
