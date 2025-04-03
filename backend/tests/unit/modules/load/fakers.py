from modules.load.domain import ports
from modules.transform.domain import value_objects as transform_value_objects


class TestSaveDataUnitOfWork(ports.AbstractDataUnitOfWork):
    def __init__(self):
        self.data = TestDataDomainRepository()

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class TestDataDomainRepository(ports.AbstractDataDomainRepository):
    def __init__(self):
        self.data: list[transform_value_objects.OutputData] = []

    def create(self, data: list[transform_value_objects.OutputData]) -> None:
        self.data.extend(data)

    def list(self) -> list[transform_value_objects.OutputData]:
        return self.data
