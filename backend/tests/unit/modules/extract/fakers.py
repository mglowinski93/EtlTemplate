from modules.extract.domain import ports, value_objects


class TestExtractUnitOfWork(ports.AbstractExtractUnitOfWork):
    def __init__(self):
        self.file: TestFileDomainRepository
        self.extract: TestExtractDomainRepository

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class TestFileDomainRepository(ports.AbstractFileDomainRepository):
    def __init__(self):
        self.saved_files: dict[str, bytes] = {}

    def save(self, file: bytes, file_name: str) -> str:
        self.saved_files[file_name] = file
        return file_name

    def file_exists(self, file_name: str) -> bool:
        return file_name in self.saved_files


class TestExtractDomainRepository(ports.AbstractExtractDomainRepository):
    def __init__(self):
        self.extract_histories: list[value_objects.ExtractHistory] = []

    def create(self, extract_history: value_objects.ExtractHistory) -> None:
        self.extract_histories.append(extract_history)

    def list(self) -> list[value_objects.ExtractHistory]:
        return self.extract_histories
