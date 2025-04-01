import pytest

from modules.load.domain import commands as domain_commands
from modules.load.services import commands as service_commands
from modules.transform.domain import value_objects as transform_value_objects
from modules.load.domain.ports import units_of_work as load_units_of_work
from modules.load.domain.ports import repositories as load_repositories

from ....common.annotations import YieldFixture
from . import fakers


def test_data_saved_successfully(test_data_unit_of_work: load_units_of_work.AbstractDataUnitOfWork, test_data_repository: load_repositories.AbstractDataDomainRepository):
    # Given
    output_data = [
        transform_value_objects.OutputData(full_name="Jessica Barnes", age=58, is_satisfied=False),
    ]
    domain_command = domain_commands.SaveData(output_data=output_data)

    # When
    service_commands.save(unit_of_work=test_data_unit_of_work, command=domain_command)

    # Then
    assert len(test_data_unit_of_work.data.data) == 1 # type: ignore[attr-defined] 
    assert all([output_data[0].full_name ==  test_data_unit_of_work.data.data[0].full_name,
                output_data[0].age ==  test_data_unit_of_work.data.data[0].age,
                output_data[0].is_satisfied ==  test_data_unit_of_work.data.data[0].is_satisfied]
            )

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
