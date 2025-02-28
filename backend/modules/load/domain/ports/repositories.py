from abc import ABC, abstractmethod

from ....data.domain import value_objects as data_value_objects


class AbstractLoadRepository(ABC):
    @abstractmethod
    def load(self, data: list[data_value_objects.OutputData]) -> None:
        """
        :param: Data to save.
        :raises DataLoadException.
        """
        pass
