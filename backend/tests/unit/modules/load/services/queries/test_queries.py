from modules.common import pagination as pagination_dtos
from modules.load.domain import value_objects
from modules.load.services import queries
from modules.load.services.queries import ports
from tests import fakers


def test_returned_data_is_of_correct_type(
    test_data_query_repository: ports.AbstractDataQueryRepository,
):
    # Given
    data_id = value_objects.DataId.new()
    test_data_query_repository.create(  # type: ignore[attr-defined]
        data=queries.DetailedOutputData(
            id=data_id,
            full_name="Johnny Bravo",
            age=1,
            is_satisfied=True,
            timestamp=fakers.fake_timestamp(),
        )
    )

    # When and then
    assert isinstance(
        queries.get_data(repository=test_data_query_repository, data_id=data_id),
        queries.DetailedOutputData,
    )


def test_returned_data_list_is_of_correct_type(
    test_data_query_repository: ports.AbstractDataQueryRepository,
):
    # Given
    data_id = value_objects.DataId.new()
    test_data_query_repository.create(  # type: ignore[attr-defined]
        data=queries.OutputData(
            id=data_id,
            full_name="Johnny Bravo",
            is_satisfied=True,
            timestamp=fakers.fake_timestamp(),
        )
    )

    # When
    results, size = queries.list_data(
        repository=test_data_query_repository,
        filters=ports.DataFilters(),
        ordering=ports.DataOrdering(),
        pagination=pagination_dtos.Pagination(
            offset=pagination_dtos.PAGINATION_DEFAULT_OFFSET,
            records_per_page=pagination_dtos.PAGINATION_DEFAULT_LIMIT,
        ),
    )

    # Then
    assert size == 1
    assert isinstance(results, list) and all(
        isinstance(item, queries.OutputData) for item in results
    )
