import logging

from modules.data.domain import value_objects as data_value_objects
from modules.load.domain.ports import repositories as domain_repositories
from modules.load.services.queries import ports as query_ports
from modules.common import pagination as pagination_dtos
from modules.common import ordering as ordering_dtos

from ...common import ordering as common_ordering

from ..models import OutputData
from .mappers import map_outputdata_model_to_output_dto

from typing import Any


logger = logging.getLogger(__name__)

#TODO move this to extract adapters
class DjangoDataDomainRepository(domain_repositories.AbstractDataDomainRepository):
    """
    See description of parent class to get more details.
    """

    def create(self, data: list[data_value_objects.OutputData]) -> None:
        OutputData.objects.bulk_create(
            [
                OutputData(
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

    def list(self,        
        filters: query_ports.OutputDataFilters,
        ordering: query_ports.OutputDataOrdering,
        pagination: pagination_dtos.Pagination,
        ) -> tuple[list[data_value_objects.OutputData], int]:
        query = OutputData.objects.filter(
            **_get_django_output_data_filters(filters)
        ).order_by(*_get_django_output_data_ordering(ordering))

        return [
            map_outputdata_model_to_output_dto(output_data)
            for output_data in query.all()[
                pagination.offset : pagination.offset + pagination.records_per_page
            ]
        ], query.count()

def _get_django_output_data_filters(filters: query_ports.OutputDataFilters) -> dict:
    django_filters: dict[str, Any] = {}

    if filters.ids is not None:
        django_filters["id__in"] = filters.ids

    if filters.full_name is not None:
        django_filters["full_name__icontains"] = filters.full_name

    if filters.age is not None:
        django_filters["age__icontains"] = filters.age

    if filters.is_satisfied is not None:
        django_filters["is_satisfied__icontains"] = filters.is_satisfied

    return django_filters


def _get_django_output_data_ordering(ordering: query_ports.OutputDataOrdering) -> list[str]:
    django_ordering: dict[str, ordering_dtos.Ordering] = {}

    if ordering.full_name is not None:
        django_ordering["full_name"] = ordering.full_name

    if ordering.age is not None:
        django_ordering["age"] = ordering.age

    if ordering.is_satisfied is not None:
        django_ordering["is_satisfied"] = ordering.is_satisfied

    return common_ordering.get_django_ordering(django_ordering)    
