import logging
from typing import Any

from modules.common import ordering as ordering_dtos
from modules.common import pagination as pagination_dtos
from modules.load.domain.ports import repositories as domain_repositories
from modules.load.services import queries as load_queries
from modules.load.services.queries import ports as query_ports

from ...common import ordering as common_ordering
from ..models import Data
from .mappers import map_data_model_to_output_data_dto

logger = logging.getLogger(__name__)


class DjangoDataDomainRepository(domain_repositories.AbstractDataDomainRepository):
    """
    See description of parent class to get more details.
    """

    def create(self, data: list[load_queries.OutputData]) -> None:
        Data.objects.bulk_create(
            [
                Data(
                    data={
                        "full_name": output_data.full_name,
                        "age": output_data.age,
                        "is_satisfied": output_data.is_satisfied,
                    }
                )
                for output_data in data
            ]
        )


class DjangoDataQueryRepository(query_ports.AbstractDataQueryRepository):
    """
    See description of parent class to get more details.
    """

    def list(
        self,
        filters: query_ports.DataFilters,
        ordering: query_ports.DataOrdering,
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


def _get_django_output_data_filters(filters: query_ports.DataFilters) -> dict:
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


def _get_django_output_data_ordering(
    ordering: query_ports.DataOrdering,
) -> list[str]:
    django_ordering: dict[str, ordering_dtos.Ordering] = {}

    if ordering.timestamp is not None:
        django_ordering["created_at"] = ordering.timestamp

    return common_ordering.get_django_ordering(django_ordering)
