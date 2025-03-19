import logging

from modules.load.services import queries as load_queries
from modules.load.services.queries import ports as query_ports
from modules.common import pagination as pagination_dtos
from modules.common import ordering as ordering_dtos

from ...common import ordering as common_ordering

from modules.load.domain.ports import repositories as domain_repositories


from ..models import Data
from .mappers import map_data_model_to_output_data_dto

from typing import Any


logger = logging.getLogger(__name__)

class DjangoDataQueryRepository(query_ports.AbstractDataQueryRepository):
    """
    See description of parent class to get more details.
    """

    def list(self,        
        filters: query_ports.OutputDataFilters,
        ordering: query_ports.OutputDataOrdering,
        pagination: pagination_dtos.Pagination,
        ) -> tuple[list[load_queries.OutputData], int]:
        query = Data.objects.filter(
            **_get_django_output_data_filters(filters)
        ).order_by(*_get_django_output_data_ordering(ordering))

        return [
            map_data_model_to_output_data_dto(output_data)
            for output_data in query.all()[
                pagination.offset : pagination.offset + pagination.records_per_page
            ]
        ], query.count()


#todo change that according to our changes in filters 
def _get_django_output_data_filters(filters: query_ports.OutputDataFilters) -> dict:
    django_filters: dict[str, Any] = {}

    if filters.age is not None:
        django_filters["data__age"] = filters.age

    if filters.is_satisfied is not None:
        django_filters["data__is_satisfied"] = filters.is_satisfied

    if filters.timestamp_from is not None:
        django_filters["created_at__gte"] = filters.timestamp_from

    if filters.timestamp_to is not None:
        django_filters["created_at__lte"] = filters.timestamp_to

    return django_filters


def _get_django_output_data_ordering(ordering: query_ports.OutputDataOrdering) -> list[str]:
    django_ordering: dict[str, ordering_dtos.Ordering] = {}

    if ordering.timestamp is not None:
        django_ordering["created_at"] = ordering.timestamp

    return common_ordering.get_django_ordering(django_ordering)    
