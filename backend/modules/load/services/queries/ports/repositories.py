from abc import abstractmethod
from typing import List

from .....common.domain import ports as common_ports
from .....data.domain import value_objects as data_value_objects


class AbstractDataQueryRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def list(self) -> tuple[List[data_value_objects.OutputData], int]:
        """
        :raises DataAccessException.
        """
        
        pass
