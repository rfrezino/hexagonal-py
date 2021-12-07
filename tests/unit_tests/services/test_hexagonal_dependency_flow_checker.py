from unittest import TestCase

from hexagonal.domain.hexagonal_project.hexagonal_project import HexagonalProject
from hexagonal.domain.hexagonal_project.hexagonal_project_layer import HexagonalProjectLayer
from hexagonal.domain.python_file import PythonFile
from hexagonal.services.hexagonal_dependency_flow_checker import HexagonalDependencyFlowChecker, DependencyFlowResponse, \
    DependencyFlowError


class TestHexagonalDependencyFlowChecker(TestCase):
    def test_check_when_project_has_files_from_different_dir_groups_in_same_layer_should_return_error(self):
        # Setup
        file1_py = PythonFile(file_full_path='/usr/src/project/adapter/lib1/file1.py',
                              file_name='file1.py',
                              file_folder_full_path='/usr/src/project/adapter/lib1/',
                              relative_folder_path_from_project_folder='/adapter/lib1',
                              project_folder_full_path='/usr/src/project',
                              imported_modules=['/usr/src/project/adapter/lib2/file2.py'])
        file2_py = PythonFile(file_full_path='/usr/src/project/adapter/lib2/file2.py',
                              file_name='file2.py',
                              file_folder_full_path='/usr/src/project/adapter/lib2/',
                              relative_folder_path_from_project_folder='/adapter/lib2',
                              project_folder_full_path='/usr/src/project', imported_modules=[])
        project = HexagonalProject(
            project_path='/usr/src/project', layers=[
                HexagonalProjectLayer(
                    index=1,
                    name='Adapters',
                    directories_groups=[['/adapter/lib1'], ['/adapter/lib2']],
                    python_files=[
                        file1_py,
                        file2_py
                    ])
            ],
            files_not_in_layers=[])

        # Execute
        dependency_checker = HexagonalDependencyFlowChecker(hexagonal_project=project)
        response = dependency_checker.check()

        # Response
        expected_result = DependencyFlowResponse(errors=[
            DependencyFlowError(
                source_file=file1_py,
                source_file_layer=HexagonalProjectLayer(
                    index=1, name='Adapters',
                    directories_groups=[['/adapter/lib1'], ['/adapter/lib2']],
                    python_files=[
                        file1_py,
                        file2_py]),
                imported_module=file2_py,
                imported_module_layer=HexagonalProjectLayer(
                    index=1,
                    name='Adapters',
                    directories_groups=[['/adapter/lib1'], ['/adapter/lib2']],
                    python_files=[file1_py,
                                  file2_py]),
                group_inter_dependency=True)])

        self.assertEqual(1, len(response.errors))
        self.assertEqual(expected_result, response)

    def test_check_when_project_is_correct_should_not_return_errors(self):
        # Setup
        project = HexagonalProject(
            project_path='/usr/src/project', layers=[
                HexagonalProjectLayer(
                    index=1,
                    name='Domain Entities',
                    directories_groups=[['/domain/entities']],
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
                    directories_groups=[['/use_case']],
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

    def test_check_when_project_is_wrong_should_return_errors(self):
        # Setup
        person_py_file = PythonFile(file_full_path='/usr/src/project/domain/entities/person.py',
                                    file_name='person.py',
                                    file_folder_full_path='/usr/src/project/domain/entities/',
                                    relative_folder_path_from_project_folder='/domain/entities',
                                    project_folder_full_path='/usr/src/project',
                                    imported_modules=['/usr/src/project/use_case/create_person.py'])
        entities_layer = HexagonalProjectLayer(
            index=1,
            name='Domain Entities',
            directories_groups=[['/domain/entities']],
            python_files=[person_py_file])

        create_person_py_file = PythonFile(file_full_path='/usr/src/project/use_case/create_person.py',
                                           file_name='create_person.py',
                                           file_folder_full_path='/usr/src/project/use_case',
                                           relative_folder_path_from_project_folder='/use_case',
                                           project_folder_full_path='/usr/src/project', imported_modules=[])
        use_case_layer = HexagonalProjectLayer(
            index=2,
            name='Use Cases',
            directories_groups=[['/use_case']],
            python_files=[create_person_py_file])

        project = HexagonalProject(
            project_path='/usr/src/project', layers=[entities_layer, use_case_layer],
            files_not_in_layers=[
                PythonFile(file_full_path='/usr/src/project/docs/out.py', file_name='out.py',
                           file_folder_full_path='/usr/src/project/docs/',
                           relative_folder_path_from_project_folder='/docs',
                           project_folder_full_path='/usr/src/project', imported_modules=[])])

        # Execute
        dependency_checker = HexagonalDependencyFlowChecker(hexagonal_project=project)
        response = dependency_checker.check()

        # Response
        expected_result = DependencyFlowResponse(
            errors=[DependencyFlowError(
                source_file=person_py_file,
                source_file_layer=entities_layer,
                imported_module=create_person_py_file,
                imported_module_layer=use_case_layer,
                group_inter_dependency=False)]
        )
        self.assertEqual(expected_result, response)
