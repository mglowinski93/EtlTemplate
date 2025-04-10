from modules.common import pagination as pagination_dtos
from modules.load.domain import ports, value_objects
from modules.load.services import queries
from modules.load.services.queries import ports as query_ports
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


class TestDataQueryRepository(query_ports.AbstractDataQueryRepository):
    def __init__(self):
        self.data = {}

    def get(self, data_id: value_objects.DataId) -> queries.DetailedOutputData:
        return self.data[data_id]

    def list(
        self,
        filters: query_ports.DataFilters,
        ordering: query_ports.DataOrdering,
        pagination: pagination_dtos.Pagination,
    ) -> tuple[list[queries.OutputData], int]:
        return list(self.data.values()), len(self.data)

    def create(self, data: queries.OutputData) -> None:
        self.data[data.id] = data
