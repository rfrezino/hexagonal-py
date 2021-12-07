from unittest import TestCase

from hexagonal.domain.hexagonal_project.hexagonal_project import HexagonalProject
from hexagonal.domain.hexagonal_project.hexagonal_project_layer import HexagonalProjectLayer
from hexagonal.domain.python_file import PythonFile
from hexagonal.services.hexagonal_dependency_flow_checker import HexagonalDependencyFlowChecker, DependencyFlowResponse, \
    DependencyFlowError


class TestHexagonalDependencyFlowChecker(TestCase):
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
                imported_module_layer=use_case_layer)]
        )
        self.assertEqual(expected_result, response)

    def test_check_when_invoicing_project_is_wrong_should_return_errors(self):
        HexagonalProject(project_path='/usr/dev/project/invoicing/invoicing', layers=[
            HexagonalProjectLayer(index=1, name='ports', directories_groups=[['/domain/ports']], python_files=[
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/ports/invoice_repository.py',
                    file_name='invoice_repository.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/ports',
                    relative_folder_path_from_project_folder='/domain/ports',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/ports/credit_repository.py',
                    file_name='credit_repository.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/ports',
                    relative_folder_path_from_project_folder='/domain/ports',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/ports/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/ports',
                    relative_folder_path_from_project_folder='/domain/ports',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/ports/event_publisher.py',
                    file_name='event_publisher.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/ports',
                    relative_folder_path_from_project_folder='/domain/ports',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[])]),
            HexagonalProjectLayer(index=2, name='api', directories_groups=[['/host']], python_files=[
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host',
                    relative_folder_path_from_project_folder='/host',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/container.py',
                    file_name='container.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host',
                    relative_folder_path_from_project_folder='/host',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/api/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/api',
                    relative_folder_path_from_project_folder='/host/api',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/api/application.py',
                    file_name='application.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/api',
                    relative_folder_path_from_project_folder='/host/api',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/api/endpoints/health.py',
                    file_name='health.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/api/endpoints',
                    relative_folder_path_from_project_folder='/host/api/endpoints',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/api/endpoints/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/api/endpoints',
                    relative_folder_path_from_project_folder='/host/api/endpoints',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/api/endpoints/invoice.py',
                    file_name='invoice.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/api/endpoints',
                    relative_folder_path_from_project_folder='/host/api/endpoints',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]),
                PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/events/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/events',
                    relative_folder_path_from_project_folder='/host/events',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/events/application.py',
                    file_name='application.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/events',
                    relative_folder_path_from_project_folder='/host/events',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/events/router.py',
                    file_name='router.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/events',
                    relative_folder_path_from_project_folder='/host/events',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/events/handlers/payments.py',
                    file_name='payments.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/events/handlers',
                    relative_folder_path_from_project_folder='/host/events/handlers',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/host/events/handlers/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/host/events/handlers',
                    relative_folder_path_from_project_folder='/host/events/handlers',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[])]),
            HexagonalProjectLayer(
                index=3, name='events', directories_groups=[['/domain/events']],
                python_files=[PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/events/invoice.py',
                    file_name='invoice.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/events',
                    relative_folder_path_from_project_folder='/domain/events',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[])]),
            HexagonalProjectLayer(
                index=4, name='use_cases', directories_groups=[['/domain/usecases']],
                python_files=[PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/usecases/get_invoice.py',
                    file_name='get_invoice.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/usecases',
                    relative_folder_path_from_project_folder='/domain/usecases',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/usecases/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/usecases',
                    relative_folder_path_from_project_folder='/domain/usecases',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/usecases/mark_invoice_sent.py',
                    file_name='mark_invoice_sent.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/usecases',
                    relative_folder_path_from_project_folder='/domain/usecases',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/usecases/add_invoice_payment.py',
                    file_name='add_invoice_payment.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/usecases',
                    relative_folder_path_from_project_folder='/domain/usecases',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[])]),
            HexagonalProjectLayer(
                index=5, name='values', directories_groups=[['/domain/values']],
                python_files=[PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/values/line_item.py',
                    file_name='line_item.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/values',
                    relative_folder_path_from_project_folder='/domain/values',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/values/invoice_payment.py',
                    file_name='invoice_payment.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/values',
                    relative_folder_path_from_project_folder='/domain/values',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/values/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/values',
                    relative_folder_path_from_project_folder='/domain/values',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/values/money.py',
                    file_name='money.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/values',
                    relative_folder_path_from_project_folder='/domain/values',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/values/invoice_number.py',
                    file_name='invoice_number.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/values',
                    relative_folder_path_from_project_folder='/domain/values',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/values/credit_number.py',
                    file_name='credit_number.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/values',
                    relative_folder_path_from_project_folder='/domain/values',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/values/domain_event.py',
                    file_name='domain_event.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/values',
                    relative_folder_path_from_project_folder='/domain/values',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[])]),
            HexagonalProjectLayer(
                index=6, name='adapters', directories_groups=[['/adapters']],
                python_files=[PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters',
                    relative_folder_path_from_project_folder='/adapters',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/publisher/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/publisher',
                    relative_folder_path_from_project_folder='/adapters/publisher',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/publisher/freshbooks.py',
                    file_name='freshbooks.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/publisher',
                    relative_folder_path_from_project_folder='/adapters/publisher',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence',
                    relative_folder_path_from_project_folder='/adapters/persistence',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/sqlite/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/sqlite',
                    relative_folder_path_from_project_folder='/adapters/persistence/sqlite',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/sqlite/invoice.py',
                    file_name='invoice.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/sqlite',
                    relative_folder_path_from_project_folder='/adapters/persistence/sqlite',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/inmemory/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/inmemory',
                    relative_folder_path_from_project_folder='/adapters/persistence/inmemory',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/inmemory/credit.py',
                    file_name='credit.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/inmemory',
                    relative_folder_path_from_project_folder='/adapters/persistence/inmemory',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/inmemory/invoice.py',
                    file_name='invoice.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/inmemory',
                    relative_folder_path_from_project_folder='/adapters/persistence/inmemory',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/mysql/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/mysql',
                    relative_folder_path_from_project_folder='/adapters/persistence/mysql',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/mysql/invoice.py',
                    file_name='invoice.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/adapters/persistence/mysql',
                    relative_folder_path_from_project_folder='/adapters/persistence/mysql',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[])]),
            HexagonalProjectLayer(
                index=7, name='entities', directories_groups=[['/domain/entities']],
                python_files=[PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/entities/__init__.py',
                    file_name='__init__.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/entities',
                    relative_folder_path_from_project_folder='/domain/entities',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/entities/entity.py',
                    file_name='entity.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/entities',
                    relative_folder_path_from_project_folder='/domain/entities',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/entities/credit.py',
                    file_name='credit.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/entities',
                    relative_folder_path_from_project_folder='/domain/entities',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[]), PythonFile(
                    file_full_path='/usr/dev/project/invoicing/invoicing/domain/entities/invoice.py',
                    file_name='invoice.py',
                    file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain/entities',
                    relative_folder_path_from_project_folder='/domain/entities',
                    project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                    imported_modules=[])])], files_not_in_layers=[
            PythonFile(file_full_path='/usr/dev/project/invoicing/invoicing/__init__.py',
                       file_name='__init__.py',
                       file_folder_full_path='/usr/dev/project/invoicing/invoicing',
                       relative_folder_path_from_project_folder='',
                       project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                       imported_modules=[]), PythonFile(
                file_full_path='/usr/dev/project/invoicing/invoicing/hexagonal_config.py',
                file_name='hexagonal_config.py',
                file_folder_full_path='/usr/dev/project/invoicing/invoicing',
                relative_folder_path_from_project_folder='',
                project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                imported_modules=[]), PythonFile(
                file_full_path='/usr/dev/project/invoicing/invoicing/domain/__init__.py',
                file_name='__init__.py',
                file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain',
                relative_folder_path_from_project_folder='/domain',
                project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                imported_modules=[]), PythonFile(
                file_full_path='/usr/dev/project/invoicing/invoicing/domain/exceptions.py',
                file_name='exceptions.py',
                file_folder_full_path='/usr/dev/project/invoicing/invoicing/domain',
                relative_folder_path_from_project_folder='/domain',
                project_folder_full_path='/usr/dev/project/invoicing/invoicing',
                imported_modules=[])])
