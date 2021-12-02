from dataclasses import dataclass
from typing import List

from hexagonal.domain.hexagonal_project.hexagonal_project import HexagonalProject
from hexagonal.domain.hexagonal_project.hexagonal_project_layer import HexagonalProjectLayer
from hexagonal.domain.python_file import PythonFile


@dataclass
class DependencyFlowError:
    source_file: PythonFile
    source_file_layer: HexagonalProjectLayer
    imported_module: PythonFile
    imported_module_layer: HexagonalProjectLayer


@dataclass
class DependencyFlowResponse:
    errors: List[DependencyFlowError]


class HexagonalDependencyFlowChecker:
    _hexagonal_project: HexagonalProject

    def __init__(self, hexagonal_project: HexagonalProject):
        self._hexagonal_project = hexagonal_project

    def check(self) -> DependencyFlowResponse:
        errors = []
        for layer in self._hexagonal_project.layers:
            errors.extend(self._check_layer(layer=layer))
        return DependencyFlowResponse(errors=errors)

    def _check_layer(self, *, layer: HexagonalProjectLayer) -> List[DependencyFlowError]:
        result = []
        for python_file in layer.python_files:
            result.extend(self._check_file(layer=layer, python_file=python_file))
        return result

    def _check_file(self, *, layer: HexagonalProjectLayer, python_file: PythonFile) -> List[DependencyFlowError]:
        result = []
        for imported_module in python_file.imported_modules:
            module_layer = self._hexagonal_project.get_layer_for_file_path(file_full_path=imported_module)
            if not module_layer:
                continue

            if layer.index < module_layer.index:
                error = DependencyFlowError(
                    source_file=python_file,
                    source_file_layer=layer,
                    imported_module=self._hexagonal_project.get_python_file(file_full_path=imported_module),
                    imported_module_layer=module_layer)
                result.append(error)

        return result
