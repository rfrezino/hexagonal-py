from typing import List

from diagrams import Diagram, Cluster
from diagrams.aws.storage import Storage

from hexagonal.hexagonal_config import HexagonalConfig


class GenerateDiagramUseCase:
    _PADDING_CHARS = 17

    def execute(self, *, project_name: str, hexagonal_config: HexagonalConfig, show: bool = False,
                output_file_name: str = '') -> bool:
        last_node = None

        with Diagram(project_name, show=show, filename=output_file_name):
            for layer in hexagonal_config.layers:
                with Cluster(self._get_adjusted_name_for_layer(cur_name=layer.name, groups=layer.directories_groups)):
                    is_first = True
                    if len(layer.directories_groups) == 1:
                        for dirs in layer.directories_groups:
                            for module in dirs:
                                cur_node = Storage(label=module)
                                if is_first:
                                    is_first = False
                                    if last_node is not None:
                                        last_node >> cur_node

                                last_node = cur_node
                    else:
                        for idx, dirs in enumerate(layer.directories_groups):
                            with Cluster(self._get_adjusted_name_for_cluster(cur_name=str(idx + 1), dirs=dirs)):
                                for module in dirs:
                                    cur_node = Storage(label=module)
                                    if is_first:
                                        is_first = False
                                        if last_node is not None:
                                            last_node >> cur_node

                                    last_node = cur_node

        return last_node is not None

    def _get_adjusted_name_for_layer(self, cur_name: str, groups: List[List[str]]) -> str:
        max_length = 0
        new_name = cur_name
        for group in groups:
            new_name = self._get_adjusted_name_for_cluster(cur_name=cur_name, dirs=group)
            if len(new_name) > max_length:
                max_length = len(new_name)

        return new_name

    def _get_adjusted_name_for_cluster(self, cur_name: str, dirs: List[str]) -> str:
        max_length = len(cur_name)
        for dir_name in dirs:
            if len(dir_name) > max_length:
                max_length = len(dir_name)

        max_length -= len(cur_name)
        return cur_name + ' ' * (max_length + self._PADDING_CHARS)
