from tests.integration_tests.utils.sample_projects.correct_clean_arch_project.infrastructure.person_mysql_repository import PersonMySqlRepository
from tests.integration_tests.utils.sample_projects.correct_clean_arch_project.usecases.create_person_usecase import CreatePersonUseCase


person_repository = PersonMySqlRepository()
use_case = CreatePersonUseCase()

use_case.execute(person_name='test_person', person_repository=person_repository)
