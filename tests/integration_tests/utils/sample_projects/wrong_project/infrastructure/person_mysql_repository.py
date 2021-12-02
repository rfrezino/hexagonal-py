from abc import abstractmethod

from tests.integration_tests.utils.sample_projects.wrong_project.domain.person import Person
from tests.integration_tests.utils.sample_projects.wrong_project.services.person_repository import PersonRepository


class PersonMySqlRepository(PersonRepository):
    @abstractmethod
    def add(self, person: Person):
        print(f'Person added {person.name}')
