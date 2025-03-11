from abc import abstractmethod
from .....data.domain import value_objects as data_value_objects
from .....common.domain import ports as common_ports
from typing import List



class AbstractDataQueryRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def list(self) -> List[data_value_objects.OutputData]:
        """
        :raises DataAccessException.
        """
        pass
