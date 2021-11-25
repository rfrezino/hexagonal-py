from abc import abstractclassmethod
from tests.unit_tests.use_cases.test_projects.correct_project.domain.person import Person
from tests.unit_tests.use_cases.test_projects.correct_project.services.person_repository import PersonRepository


class PersonMySqlRepository(PersonRepository):
    @abstractclassmethod
    def add(self, person: Person):
        print(f'Person added {person.name}')
    
    