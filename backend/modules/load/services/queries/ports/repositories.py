from abc import abstractmethod
from typing import List

from .....common.domain import ports as common_ports
from .dtos import OutputData


class AbstractDataQueryRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def list(self) -> tuple[List[OutputData], int]:
        """
        :raises DataAccessException.
        """

        pass
