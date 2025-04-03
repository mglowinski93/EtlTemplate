import pytest

from modules.load.domain import commands as domain_commands
from modules.load.domain import ports
from modules.load.services import commands as service_commands
from modules.transform.domain import value_objects as transform_value_objects

from ....common.annotations import YieldFixture
from .fakers import TestDataDomainRepository, TestSaveDataUnitOfWork


def test_data_saved_successfully(
    test_data_unit_of_work: ports.AbstractDataUnitOfWork,
):
    # Given
    output_data = [
        transform_value_objects.OutputData(
            full_name="Jessica Barnes", age=58, is_satisfied=False
        ),
    ]
    domain_command = domain_commands.SaveData(output_data=output_data)

    # When
    service_commands.save(unit_of_work=test_data_unit_of_work, command=domain_command)

    # Then
    assert len(test_data_unit_of_work.data.data) == 1  # type: ignore[attr-defined]
    assert all(
        [
            output_data[0].full_name == test_data_unit_of_work.data.data[0].full_name,  # type: ignore[attr-defined]
            output_data[0].age == test_data_unit_of_work.data.data[0].age,  # type: ignore[attr-defined]
            output_data[0].is_satisfied
            == test_data_unit_of_work.data.data[0].is_satisfied,  # type: ignore[attr-defined]
        ]
    )


@pytest.fixture
def test_data_repository() -> YieldFixture[TestDataDomainRepository]:
    yield TestDataDomainRepository()


@pytest.fixture
def test_data_unit_of_work(
    test_data_repository,
) -> YieldFixture[TestSaveDataUnitOfWork]:
    test_unit_of_work = TestSaveDataUnitOfWork()
    test_unit_of_work.data = test_data_repository
    yield test_unit_of_work
