from abc import abstractmethod

from ....common.domain import ports as common_ports
from ...services import queries as load_queries


class AbstractDataDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def create(self, data: list[load_queries.OutputData]) -> None:
        """
        :param: Data to save.
        """

        pass
