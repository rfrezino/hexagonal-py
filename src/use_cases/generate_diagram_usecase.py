from typing import List

from diagrams import Diagram, Cluster
from diagrams.aws.storage import Storage

from domain.hexagonal_layer import HexagonalLayer


class GenerateDiagramUseCase:

    @staticmethod
    def execute(*, project_name: str, hexagonal_composition: List[HexagonalLayer]) -> bool:
        last_node = None
        with Diagram(project_name):
            for layer in hexagonal_composition:
                with Cluster(layer.name):
                    is_first = True
                    for module in layer.directories:
                        cur_node = Storage(label=module)
                        if is_first:
                            is_first = False
                            if last_node is not None:
                                last_node >> cur_node

                        last_node = cur_node

        return last_node is not None
