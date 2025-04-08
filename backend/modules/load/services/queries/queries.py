from .dtos import DetailedOutputData, OutputData
from . import ports
from ...domain import value_objects
from ....common import pagination as pagination_dtos
from ....common import ordering as common_ordering


def get_data(
    repository: ports.AbstractDataQueryRepository,
    data_id: value_objects.DataId,
) -> DetailedOutputData:
    return repository.get(data_id)


def list_data(
    repository: ports.AbstractDataQueryRepository,
    filters: ports.DataFilters | None = None,
    ordering: ports.DataOrdering | None = None,
    pagination: pagination_dtos.Pagination | None = None,
) -> tuple[list[OutputData], int]:
    if filters is None:
        filters = ports.DataFilters()

    if ordering is None:
        ordering = ports.DataOrdering(
            timestamp=common_ordering.Ordering(order=common_ordering.OrderingOrder.DESCENDING, priority=1),
        )

    if pagination is None:
        pagination = pagination_dtos.Pagination(
            offset=pagination_dtos.PAGINATION_DEFAULT_OFFSET,
            records_per_page=pagination_dtos.PAGINATION_DEFAULT_LIMIT,
        )

    return repository.list(
        filters=filters,
        ordering=ordering,
        pagination=pagination,
    )
