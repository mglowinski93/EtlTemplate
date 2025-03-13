from abc import abstractmethod

from ....common.domain import ports as common_ports
from ....data.domain import value_objects as data_value_objects


class AbstractDataDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def create(self, data: list[data_value_objects.OutputData]) -> None:
        """
        :param: Data to save.
        :raises DataCreationException.
        """
        pass
