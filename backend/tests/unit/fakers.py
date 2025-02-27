from modules.load.domain.ports import repositories as domain_repositories
from modules.load.domain.ports import units_of_work as domain_uow
from modules.data.domain import value_objects as data_value_objects

class TestLoadUnitOfWork(domain_uow.AbstractLoadUnitOfWork):
    def __init__(self, repository: domain_repositories.AbstractLoadRepository):
        self.repository = repository

    def load(self, output_data: list[data_value_objects.OutputData]):
        self.repository.load(output_data)       

    def __enter__(self):
        return self

    def __exit__(self):
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class TestLoadRepository(domain_repositories.AbstractLoadRepository):
    in_memory_db: list[data_value_objects.OutputData] = []

    def load(self, data: list[data_value_objects.OutputData]) -> None:
        self.in_memory_db.extend(data)
