import pytest

from modules.load.domain import commands as domain_commands
from modules.load.services import commands as service_commands
from modules.load.services import queries as load_queries

from ....common.annotations import YieldFixture
from ... import fakers


def test_data_saved_successfully(test_data_unit_of_work, test_data_repository):
    # Given
    output_dataset_rows = 3
    output_data = [
        load_queries.OutputData(full_name="Jessica Barnes", age=58, is_satisfied=False),
        load_queries.OutputData(
            full_name="Jennifer Ferguson", age=62, is_satisfied=False
        ),
        load_queries.OutputData(
            full_name="Shannon Gonzales", age=36, is_satisfied=True
        ),
    ]
    domain_command = domain_commands.SaveData(output_data=output_data)

    # When
    service_commands.save(unit_of_work=test_data_unit_of_work, command=domain_command)

    # Then
    assert len(test_data_repository.list()) == output_dataset_rows
    assert test_data_repository.list()[1] == output_data[1]


@pytest.fixture
def test_data_repository() -> YieldFixture[fakers.TestDataDomainRepository]:
    yield fakers.TestDataDomainRepository()


@pytest.fixture
def test_data_unit_of_work(
    test_data_repository,
) -> YieldFixture[fakers.TestSaveDataUnitOfWork]:
    test_unit_of_work = fakers.TestSaveDataUnitOfWork()
    test_unit_of_work.data = test_data_repository
    yield test_unit_of_work
