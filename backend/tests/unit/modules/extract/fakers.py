from pathlib import Path
from modules.extract.domain.ports import repositories
from modules.extract.domain.ports import units_of_work
from modules.extract.domain import value_objects
from tests import test_const 

#todo use this instead of global faker.py
class TestExtractUnitOfWork(units_of_work.AbstractExtractUnitOfWork):
    def __init__(self):
        self.file: TestFileDomainRepository
        self.extract: TestExtractDomainRepository

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

class TestFileDomainRepository(repositories.AbstractFileDomainRepository):
    def __init__(self):
        self.saved_files : dict[Path, bytes] = {}
        
    def save(self, file: bytes, file_name: str) -> Path:
        self.saved_files[test_const.EXTRACT_TEST_FILES_LOCATION / file_name] = file
        return test_const.EXTRACT_TEST_FILES_LOCATION / file_name
    
    def file_exists(self, file_path: Path) -> bool:
        return file_path in self.saved_files
        
    
class TestExtractDomainRepository(repositories.AbstractExtractDomainRepository):
    def __init__(self):
        self.extract_histories: list[value_objects.ExtractHistory] = []

    def create(self, extract_history: value_objects.ExtractHistory) -> None:
        self.extract_histories.append(extract_history)

    def list(self) -> list[value_objects.ExtractHistory]:
        return self.extract_histories
