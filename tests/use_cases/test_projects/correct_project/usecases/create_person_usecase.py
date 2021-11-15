from tests.use_cases.test_projects.correct_project.domain.person import Person
from tests.use_cases.test_projects.correct_project.services.person_repository import PersonRepository


class CreatePersonUseCase():
    def execute(self, person_name: str, person_repository: PersonRepository):
        person = Person()
        person.name = person_name
        
        person_repository.add(person=person)        
        