from abc import abstractmethod
from pathlib import Path

from ....common.domain import ports as common_ports


class AbstractFileDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def save(self, file_bytes: bytes, file_name: str) -> Path:
        """
        :param: File as bytes.
        :raises FileSaveException.
        """
        pass
