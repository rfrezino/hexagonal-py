from abc import ABCMeta, abstractmethod

from tests.test_projects.wrong_project.domain.person import Person


class PersonRepository(ABCMeta):
    @abstractmethod
    def add(self, person: Person):
        ...
