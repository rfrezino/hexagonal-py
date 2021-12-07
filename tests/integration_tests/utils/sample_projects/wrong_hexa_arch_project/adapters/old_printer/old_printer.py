from tests.integration_tests.utils.sample_projects.correct_hexa_arch_project.domain.file_content import FileContent
from tests.integration_tests.utils.sample_projects.correct_hexa_arch_project.port.printer import PrinterInterface


class OldPrinter(PrinterInterface):
    def print_file(self, file: FileContent):
        print(file.content)
