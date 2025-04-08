from modules.common import pagination as pagination_dtos
from modules.load.domain import value_objects
from modules.load.services import queries
from modules.load.services.queries import ports


def test_returned_data_is_of_correct_type(
    test_data_query_repository: ports.AbstractDataQueryRepository,
):
    # When and then
    isinstance(
        queries.get_data(
            repository=test_data_query_repository, data_id=value_objects.DataId.new()
        ),
        queries.DetailedOutputData,
    )


def test_returned_data_list_is_of_correct_type(
    test_data_query_repository: ports.AbstractDataQueryRepository,
):
    # When
    results = queries.list_data(
        repository=test_data_query_repository,
        filters=ports.DataFilters(),
        ordering=ports.DataOrdering(),
        pagination=pagination_dtos.Pagination(
            offset=pagination_dtos.PAGINATION_DEFAULT_OFFSET,
            records_per_page=pagination_dtos.PAGINATION_DEFAULT_LIMIT,
        ),
    )
    # When and then
    isinstance(results, list) and all(
        isinstance(item, queries.DetailedOutputData) for item in results
    )
