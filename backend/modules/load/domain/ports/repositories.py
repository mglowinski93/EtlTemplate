from abc import ABC, abstractmethod

from ....data.domain import value_objects as data_value_objects


class AbstractDataDomainRepository(ABC):
    @abstractmethod
    def create(self, data: list[data_value_objects.OutputData]) -> None:
        """
        :param: Data to save.
        :raises DataCreationException.
        """
        pass
