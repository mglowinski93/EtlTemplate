from abc import abstractmethod

from .....common import pagination as pagination_dtos
from .....common.domain import ports as common_ports
from ..dtos import OutputData
from .dtos import DataFilters, DataOrdering


class AbstractDataQueryRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def list(
        self,
        filters: DataFilters,
        ordering: DataOrdering,
        pagination: pagination_dtos.Pagination,
    ) -> tuple[list[OutputData], int]:
        """
        :raises DataAccessException.
        """
        pass
