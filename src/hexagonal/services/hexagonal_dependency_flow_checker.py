from typing import List

from hexagonal.domain.python_file import PythonFile
from hexagonal.services.hexagonal_composition import HexagonalComposition


class HexagonalDependencyFlowChecker:
    _python_files: List[PythonFile]
    _composition: HexagonalComposition

    def __init__(self, python_files: List[PythonFile], composition: HexagonalComposition):
        self._python_files = python_files
        self._composition = composition

    def check(self):
        pass

    def
