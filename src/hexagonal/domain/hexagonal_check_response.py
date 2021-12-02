from typing import List

from hexagonal.domain.hexagonal_error import HexagonalError
from hexagonal.domain.python_file import PythonFile


class HexagonalCheckResponse:
    errors: List[HexagonalError]
    python_files: List[PythonFile]
