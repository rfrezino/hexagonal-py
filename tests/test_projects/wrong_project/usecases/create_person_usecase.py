from tests.test_projects.wrong_project.domain.person import Person
from tests.test_projects.wrong_project.infrastructure.person_mysql_repository import PersonMySqlRepository


class CreatePersonUseCase():
    def execute(self, person_name: str, person_repository: PersonMySqlRepository):
        person = Person()
        person.name = person_name

        person_repository.add(person=person)
