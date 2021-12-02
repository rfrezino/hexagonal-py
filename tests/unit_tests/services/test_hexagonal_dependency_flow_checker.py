from unittest import TestCase

from hexagonal.domain.hexagonal_project.hexagonal_project import HexagonalProject
from hexagonal.domain.hexagonal_project.hexagonal_project_layer import HexagonalProjectLayer
from hexagonal.domain.python_file import PythonFile
from hexagonal.services.hexagonal_dependency_flow_checker import HexagonalDependencyFlowChecker, DependencyFlowResponse


class TestHexagonalDependencyFlowChecker(TestCase):
    def test_check_when_project_is_correct_should_not_return_errors(self):
        # Setup
        project = HexagonalProject(
            project_path='/usr/src/project', layers=[
                HexagonalProjectLayer(
                    index=1,
                    name='Domain Entities',
                    directories=['/domain/entities'],
                    python_files=[
                        PythonFile(file_full_path='/usr/src/project/domain/entities/person.py',
                                   file_name='person.py',
                                   file_folder_full_path='/usr/src/project/domain/entities/',
                                   relative_folder_path_from_project_folder='/domain/entities',
                                   project_folder_full_path='/usr/src/project',
                                   imported_modules=[])]),
                HexagonalProjectLayer(
                    index=2,
                    name='Use Cases',
                    directories=['/use_case'],
                    python_files=[
                        PythonFile(file_full_path='/usr/src/project/use_case/create_person.py',
                                   file_name='create_person.py',
                                   file_folder_full_path='/usr/src/project/use_case',
                                   relative_folder_path_from_project_folder='/use_case',
                                   project_folder_full_path='/usr/src/project',
                                   imported_modules=['/usr/src/project/domain/entities/person.py'])])],
            files_not_in_layers=[
                PythonFile(file_full_path='/usr/src/project/docs/out.py', file_name='out.py',
                           file_folder_full_path='/usr/src/project/docs/',
                           relative_folder_path_from_project_folder='/docs',
                           project_folder_full_path='/usr/src/project', imported_modules=[])])

        # Execute
        dependency_checker = HexagonalDependencyFlowChecker(hexagonal_project=project)
        response = dependency_checker.check()

        # Response
        expected_result = DependencyFlowResponse(errors=[])
        self.assertEqual(expected_result, response)
