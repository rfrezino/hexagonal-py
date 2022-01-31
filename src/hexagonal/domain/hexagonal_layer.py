import os
from dataclasses import dataclass
from typing import List


@dataclass
class HexagonalLayer:
    name: str
    directories_groups: List[List[str]]

    def __post_init__(self):
        self._valid_dirs()

    def _valid_dirs(self):
        for dirs in self.directories_groups:
            for dir in dirs:
                if not dir.startswith('/'):
                    raise Exception(f'Hexagonal Layer directory "{self.name}" must start with /. Example: "/domain"')

                if dir.endswith('/'):
                    raise Exception(
                        f'Hexagonal Layer directory "{self.name}" must not finish with /. Example: "/domain"')
