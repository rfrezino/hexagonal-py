from typing import List

from hexagonal.domain.hexagonal_error import HexagonalError
from hexagonal.domain.python_project import PythonProject


class HexagonalCheckResponse:
    errors: List[HexagonalError]
    project: PythonProject
