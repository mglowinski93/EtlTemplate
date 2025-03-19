from modules.load.services import queries as load_queries
from modules.load.domain.ports import repositories as domain_repositories
from modules.load.domain.ports import units_of_work as domain_uow


class TestSaveDataUnitOfWork(domain_uow.AbstractDataUnitOfWork):
    def __init__(self):
        self.data = TestDataDomainRepository()

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class TestDataDomainRepository(domain_repositories.AbstractDataDomainRepository):
    def __init__(self):
        self.data: list[load_queries.OutputData] = []

    def create(self, data: list[load_queries.OutputData]) -> None:
        self.data.extend(data)

    def list(self) -> list[load_queries.OutputData]:
        return self.data
