from typing import List
from unittest import TestCase

from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.domain.hexagonal_project.hexagonal_project import HexagonalProject
from hexagonal.domain.hexagonal_project.hexagonal_project_layer import HexagonalProjectLayer
from hexagonal.domain.python_file import PythonFile
from hexagonal.services.hexagonal_composition import HexagonalComposition
from hexagonal.services.hexagonal_project_builder import HexagonalProjectBuilder


class TestHexagonalProjectBuilder(TestCase):
    def test_build_when_params_are_valid_result_valid_response(self):
        # Setup
        python_files: List[PythonFile] = [
            PythonFile(file_full_path='/usr/src/project/domain/entities/person.py',
                       file_name='person.py',
                       file_folder_full_path='/usr/src/project/domain/entities/',
                       relative_folder_path_from_project_folder='/domain/entities',
                       project_folder_full_path='/usr/src/project',
                       imported_modules=[]
                       ),
            PythonFile(file_full_path='/usr/src/project/use_case/create_person.py',
                       file_name='create_person.py',
                       file_folder_full_path='/usr/src/project/use_case',
                       relative_folder_path_from_project_folder='/use_case',
                       project_folder_full_path='/usr/src/project',
                       imported_modules=[]
                       ),
            PythonFile(file_full_path='/usr/src/project/docs/out.py',
                       file_name='out.py',
                       file_folder_full_path='/usr/src/project/docs/',
                       relative_folder_path_from_project_folder='/docs',
                       project_folder_full_path='/usr/src/project',
                       imported_modules=[]
                       )
        ]
        hexagonal_composition = HexagonalComposition()
        entities = HexagonalLayer(name='Domain Entities', directories_groups=[['/domain/entities']])
        use_cases = HexagonalLayer(name='Use Cases', directories_groups=[['/use_case']])
        hexagonal_composition + use_cases >> entities

        entities_layer = HexagonalProjectLayer(
            index=1,
            name='Domain Entities',
            directories_groups=[['/domain/entities']],
            python_files=[
                PythonFile(file_full_path='/usr/src/project/domain/entities/person.py',
                           file_name='person.py',
                           file_folder_full_path='/usr/src/project/domain/entities/',
                           relative_folder_path_from_project_folder='/domain/entities',
                           project_folder_full_path='/usr/src/project',
                           imported_modules=[])])

        use_cases_layer = HexagonalProjectLayer(
            index=2,
            name='Use Cases',
            directories_groups=[['/use_case']],
            python_files=[
                PythonFile(file_full_path='/usr/src/project/use_case/create_person.py',
                           file_name='create_person.py',
                           file_folder_full_path='/usr/src/project/use_case',
                           relative_folder_path_from_project_folder='/use_case',
                           project_folder_full_path='/usr/src/project',
                           imported_modules=[])])

        expected_result = HexagonalProject(
            project_path='/usr/src/project', layers=[entities_layer, use_cases_layer],
            files_not_in_layers=[
                PythonFile(file_full_path='/usr/src/project/docs/out.py', file_name='out.py',
                           file_folder_full_path='/usr/src/project/docs/',
                           relative_folder_path_from_project_folder='/docs',
                           project_folder_full_path='/usr/src/project', imported_modules=[])])

        # Execute
        builder = HexagonalProjectBuilder(python_files=python_files, hexagonal_composition=hexagonal_composition)
        response_project = builder.build()

        # Assert
        self.assertEqual(expected_result, response_project)

    def test_build_when_layers_has_nested_folder_and_are_valid_result_valid_response(self):
        # Setup
        invoice_py_file = PythonFile(file_full_path='/usr/src/invoicing/adapters/persistence/mysql/invoice.py',
                                     file_name='invoice.py',
                                     file_folder_full_path='/usr/src/invoicing/adapters/persistence/mysql',
                                     relative_folder_path_from_project_folder='/adapters/persistence/mysql',
                                     project_folder_full_path='/usr/src/invoicing', imported_modules=[])

        hexagonal_composition = HexagonalComposition()
        adapters = HexagonalLayer(name='Adapters', directories_groups=[['/adapters']])
        hexagonal_composition + adapters

        # Execute
        builder = HexagonalProjectBuilder(python_files=[invoice_py_file], hexagonal_composition=hexagonal_composition)
        response_project = builder.build()

        # Assert
        expected_result = HexagonalProject(
            project_path='/usr/src/invoicing',
            layers=[
                HexagonalProjectLayer(index=1, name='Adapters', directories_groups=[['/adapters']],
                                      python_files=[invoice_py_file])],
            files_not_in_layers=[])

        self.assertEqual(expected_result, response_project)
