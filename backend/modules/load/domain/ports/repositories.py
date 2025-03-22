import io
from abc import abstractmethod
from pathlib import Path

from ....common.domain import ports as common_ports
from ...services import queries as load_queries


class AbstractDataDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def create(self, data: list[load_queries.OutputData]) -> None:
        """
        :param: Data to save.
        :raises DataCreationException.
        """
        pass

class AbstractFileSaveRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def save(self, bytes: io.BytesIO, file_name: str) -> Path:
        """
        :param: File as bytes.
        :raises Path where file is saved.
        """
        pass
