from abc import ABC, abstractmethod

from tests.integration_tests.utils.sample_projects.correct_hexa_arch_project.domain.file_content import FileContent


class PrinterInterface(metaclass=ABC):
    @abstractmethod
    def print_file(self, file: FileContent):
        pass
