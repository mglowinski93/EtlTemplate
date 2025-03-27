from abc import abstractmethod

from ....common.domain import ports as common_ports
from ....transform.domain import value_objects as domain_value_objects


class AbstractDataDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def create(self, data: list[domain_value_objects.OutputData]) -> None:
        """
        :param: Data to save.
        """

        pass
