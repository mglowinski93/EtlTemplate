from abc import abstractmethod

from .....common.domain import ports as common_ports
from .dtos import OutputData


class AbstractDataQueryRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def list(self) -> tuple[list[OutputData], int]:
        """
        :raises DataAccessException.
        """

        pass
