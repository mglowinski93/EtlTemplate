from modules.common import pagination as pagination_dtos
from modules.extract.domain import ports as extract_ports
from modules.extract.domain import value_objects as extract_value_objects
from modules.load.domain import ports as load_ports
from modules.load.domain import value_objects as load_value_objects
from modules.load.services import queries
from modules.load.services.queries import ports as query_ports
from modules.transform.domain import value_objects as transform_value_objects


class TestExtractUnitOfWork(extract_ports.AbstractExtractUnitOfWork):
    def __init__(self):
        self.file = TestFileDomainRepository()
        self.extract = TestExtractDomainRepository()

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class TestFileDomainRepository(extract_ports.AbstractFileDomainRepository):
    def __init__(self):
        self.saved_files: dict[str, bytes] = {}

    def save(self, file: bytes, file_name: str) -> str:
        self.saved_files[file_name] = file
        return file_name

    def file_exists(self, file_name: str) -> bool:
        return file_name in self.saved_files


class TestExtractDomainRepository(extract_ports.AbstractExtractDomainRepository):
    def __init__(self):
        self.extract_histories: list[extract_value_objects.ExtractHistory] = []

    def create(self, extract_history: extract_value_objects.ExtractHistory) -> None:
        self.extract_histories.append(extract_history)

    def list(self) -> list[extract_value_objects.ExtractHistory]:
        return self.extract_histories


class TestSaveDataUnitOfWork(load_ports.AbstractDataUnitOfWork):
    def __init__(self):
        self.data = TestDataDomainRepository()

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class TestDataDomainRepository(load_ports.AbstractDataDomainRepository):
    def __init__(self):
        self.data: list[transform_value_objects.TransformedData] = []

    def create(self, data: list[transform_value_objects.TransformedData]) -> None:
        self.data.extend(data)

    def list(self) -> list[transform_value_objects.TransformedData]:
        return self.data


class TestDataQueryRepository(query_ports.AbstractDataQueryRepository):
    def __init__(self):
        self.data = {}

    def get(self, data_id: load_value_objects.DataId) -> queries.DetailedOutputData:
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
