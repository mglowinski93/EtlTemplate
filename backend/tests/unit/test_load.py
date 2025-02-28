from modules.data.domain import value_objects as data_value_objects
from modules.load.domain import commands as domain_commands
from modules.load.domain.ports import repositories as domain_repositories
from modules.load.domain.ports import units_of_work as domain_uow
from modules.load.services import commands as service_commands


def test_data_loaded_successfully():
    # Given
    output_dataset_rows = 3
    output_data = [
        data_value_objects.OutputData(
            full_name="Jessica Barnes", age=58, is_satisfied=False
        ),
        data_value_objects.OutputData(
            full_name="Jennifer Ferguson", age=62, is_satisfied=False
        ),
        data_value_objects.OutputData(
            full_name="Shannon Gonzales", age=36, is_satisfied=True
        ),
    ]
    domain_command = domain_commands.LoadData(output_data=output_data)

    fake_repository: domain_repositories.AbstractLoadRepository = FakeRepository()
    fake_unit_of_work: domain_uow.AbstractLoadUnitOfWork = FakeUnitOfWork(fake_repository)

    # When
    service_commands.load(domain_command, fake_unit_of_work)

    # Then
    assert len(fake_repository.in_memory_db) == output_dataset_rows
    assert fake_repository.in_memory_db[1] == output_data[1]
    assert fake_unit_of_work.committed


class FakeUnitOfWork(domain_uow.AbstractLoadUnitOfWork):
    def __init__(self, repository: domain_repositories.AbstractLoadRepository):
        self.repository = repository

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


class FakeRepository(domain_repositories.AbstractLoadRepository):
    in_memory_db: list[data_value_objects.OutputData] = []

    def load(self, data: list[data_value_objects.OutputData]) -> None:
        self.in_memory_db.extend(data)
