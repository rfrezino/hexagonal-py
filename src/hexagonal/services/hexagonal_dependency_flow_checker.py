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
    group_inter_dependency: bool



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

    @staticmethod
    def _is_inner_layer_is_point_to_outer_layer(inner_layer: HexagonalProjectLayer,
                                                outer_layer: HexagonalProjectLayer) -> bool:
        return inner_layer.index < outer_layer.index

    def _are_files_in_same_layer(self, source_layer: HexagonalProjectLayer,
                                 module_layer: HexagonalProjectLayer) -> bool:
        return source_layer.index == module_layer.index

    @staticmethod
    def _is_source_file_pointer_to_file_in_different_dir_group(source_file: PythonFile,
                                                               module: PythonFile,
                                                               layer: HexagonalProjectLayer) -> bool:
        source_file_dir_id = layer.get_directory_group_index_for_file(
            relative_folder_path_from_project_folder=source_file.relative_folder_path_from_project_folder)
        module_dir_id = layer.get_directory_group_index_for_file(
            relative_folder_path_from_project_folder=module.relative_folder_path_from_project_folder
        )

        return source_file_dir_id != module_dir_id

    def _check_file(self, *, layer: HexagonalProjectLayer, python_file: PythonFile) -> List[DependencyFlowError]:
        result = []
        for imported_module_path in python_file.imported_modules:
            module_layer = self._hexagonal_project.get_layer_for_file_path(file_full_path=imported_module_path)
            if not module_layer:
                continue

            imported_module = self._hexagonal_project.get_python_file(file_full_path=imported_module_path)

            if self._is_inner_layer_is_point_to_outer_layer(inner_layer=layer, outer_layer=module_layer):
                error = DependencyFlowError(
                    source_file=python_file,
                    source_file_layer=layer,
                    imported_module=imported_module,
                    imported_module_layer=module_layer,
                    group_inter_dependency=False)
                result.append(error)
                continue

            if self._are_files_in_same_layer(source_layer=layer, module_layer=module_layer):
                if self._is_source_file_pointer_to_file_in_different_dir_group(source_file=python_file,
                                                                               module=imported_module,
                                                                               layer=layer):
                    error = DependencyFlowError(
                        source_file=python_file,
                        source_file_layer=layer,
                        imported_module=imported_module,
                        imported_module_layer=module_layer,
                        group_inter_dependency=True)
                    result.append(error)

        return result
