from dataclasses import dataclass


@dataclass
class HexagonalError:
    message: str
    outer_layer_name: str
    inner_layer_name: str
    python_file_problem: str
    imported_module_problem: str