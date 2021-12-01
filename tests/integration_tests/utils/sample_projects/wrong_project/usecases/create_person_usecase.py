from tests.integration_tests.utils.sample_projects.wrong_project.domain.person import Person
from tests.integration_tests.utils.sample_projects.wrong_project.infrastructure.person_mysql_repository import PersonMySqlRepository


class CreatePersonUseCase():
    # Here is the error, I'm point to an outer layer, from usecases to infrastructure
    def execute(self, person_name: str, person_repository: PersonMySqlRepository):
        person = Person()
        person.name = person_name

        person_repository.add(person=person)
