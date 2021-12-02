from typing import List

from hexagonal.domain.hexagonal_project.hexagonal_project import HexagonalProject
from hexagonal.domain.hexagonal_project.hexagonal_project_layer import HexagonalProjectLayer
from hexagonal.domain.python_file import PythonFile
from hexagonal.services.hexagonal_composition import HexagonalComposition


class HexagonalProjectBuilder:
    _python_files: List[PythonFile]
    _project_folder_full_path: str

    def __init__(self, python_files: List[PythonFile], hexagonal_composition: HexagonalComposition):
        self._python_files = python_files
        self._hexagonal_composition = hexagonal_composition

    def build(self) -> HexagonalProject:
        if not self._python_files:
            raise Exception('No python files found.')

        self._project_folder_full_path = self._extract_project_path()
        project_layers = self._generate_layers()
        self._add_files_to_corresponding_layers(project_layers=project_layers)
        files_not_in_layers = self._get_files_without_layers(project_layers=project_layers)

        return HexagonalProject(project_path=self._project_folder_full_path,
                                layers=project_layers,
                                files_not_in_layers=files_not_in_layers)

    def _extract_project_path(self) -> str:
        return self._python_files[0].project_folder_full_path

    def _generate_layers(self) -> List[HexagonalProjectLayer]:
        result = []
        for idx, composition_layer in enumerate(reversed(self._hexagonal_composition)):
            project_layer = HexagonalProjectLayer(
                index=idx + 1,
                name=composition_layer.name,
                directories=composition_layer.directories,
                python_files=[]
            )
            result.append(project_layer)

        result.sort(key=lambda item: item.index)
        return result

    def _add_files_to_corresponding_layers(self, project_layers: List[HexagonalProjectLayer]):
        for python_file in self._python_files:
            for layer in project_layers:
                relative_path = python_file.relative_folder_path_from_project_folder
                if any(relative_path.startswith(layer_dir) for layer_dir in layer.directories):
                    layer.python_files.append(python_file)
                    break

    def _get_files_without_layers(self, project_layers: List[HexagonalProjectLayer]) -> List[PythonFile]:
        result = []
        for python_file in self._python_files:
            file_add = False
            for layer in project_layers:
                relative_path = python_file.relative_folder_path_from_project_folder
                if any(relative_path.startswith(layer_dir) for layer_dir in layer.directories):
                    file_add = True
                    break

            if not file_add:
                result.append(python_file)

        return result
