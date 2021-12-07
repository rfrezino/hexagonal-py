from abc import ABCMeta, abstractmethod

from tests.integration_tests.utils.sample_projects.wrong_clean_arch_project.domain.person import Person


class PersonRepository(ABCMeta):
    @abstractmethod
    def add(self, person: Person):
        ...
