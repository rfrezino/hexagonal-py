from typing import List

from domain.hexagonal_error import HexagonalError
from domain.python_project import PythonProject


class HexagonalCheckResponse:
    errors: List[HexagonalError]
    project: PythonProject
