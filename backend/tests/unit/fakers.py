from modules.load.domain.ports import repositories as domain_repositories
from modules.load.domain.ports import units_of_work as domain_uow
from modules.transform.domain import value_objects as transform_value_objects


class TestSaveDataUnitOfWork(domain_uow.AbstractDataUnitOfWork):
    def __init__(self):
        self.data = TestDataDomainRepository()

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class TestDataDomainRepository(domain_repositories.AbstractDataDomainRepository):
    def __init__(self):
        self.data: list[transform_value_objects.OutputData] = []

    def create(self, data: list[transform_value_objects.OutputData]) -> None:
        self.data.extend(data)

    def list(self) -> list[transform_value_objects.OutputData]:
        return self.data
