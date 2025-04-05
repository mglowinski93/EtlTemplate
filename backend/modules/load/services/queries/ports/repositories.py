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
        :param filters: Filters to apply to data.
        :param ordering: Ordering to apply to data.
        :param pagination: Pagination to apply to data.
        :raises: DatabaseError: Failed to query output data.

        :return: List of all output data and
                count of reservations matching given filters.
        """

        pass
