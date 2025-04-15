import logging
from typing import Any

from django.db import DatabaseError

from modules.common import ordering as ordering_dtos
from modules.common import pagination as pagination_dtos
from modules.load.domain import ports, value_objects
from modules.load.services import queries
from modules.load.services.queries import ports as query_ports
from modules.transform.domain import value_objects as transform_value_objects

from ...common import exceptions as common_exceptions
from ...common import ordering as common_ordering
from ..models import Data
from .mappers import (
    map_data_model_to_detailed_output_data_dto,
    map_data_model_to_output_data_dto,
    map_transformed_data_to_data_field,
)

logger = logging.getLogger(__name__)


class DjangoDataDomainRepository(ports.AbstractDataDomainRepository):
    """
    See description of parent class to get more details.
    """

    def create(self, data: list[transform_value_objects.TransformedData]) -> None:
        try:
            Data.objects.bulk_create(
                [Data(data=map_transformed_data_to_data_field(_data)) for _data in data]
            )
        except DatabaseError as err:
            logger.exception(err)
            raise common_exceptions.DatabaseError("Database connection issue.") from err


class DjangoDataQueryRepository(query_ports.AbstractDataQueryRepository):
    """
    See description of parent class to get more details.
    """

    def get(self, data_id: value_objects.DataId) -> queries.DetailedOutputData:
        try:
            return map_data_model_to_detailed_output_data_dto(
                Data.objects.get(id=data_id)
            )
        except Data.DoesNotExist as err:
            logger.exception(err)
            raise common_exceptions.DataDoesNotExist("Data not found.") from err
        except DatabaseError as err:
            logger.exception(err)
            raise common_exceptions.DatabaseError("Database connection issue.") from err

    def list(
        self,
        filters: query_ports.DataFilters,
        ordering: query_ports.DataOrdering,
        pagination: pagination_dtos.Pagination,
    ) -> tuple[list[queries.OutputData], int]:
        try:
            query = Data.objects.filter(
                **_get_django_output_data_filters(filters)
            ).order_by(*_get_django_output_data_ordering(ordering))
        except DatabaseError as err:
            logger.exception(err)
            raise common_exceptions.DatabaseError("Database connection issue.") from err

        return [
            map_data_model_to_output_data_dto(output_data)
            for output_data in query.all()[
                pagination.offset : pagination.offset + pagination.records_per_page
            ]
        ], query.count()


def _get_django_output_data_filters(filters: query_ports.DataFilters) -> dict:
    django_filters: dict[str, Any] = {}

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

    if ordering.full_name is not None:
        django_ordering["data__full_name"] = ordering.full_name

    return common_ordering.get_django_ordering(django_ordering)
