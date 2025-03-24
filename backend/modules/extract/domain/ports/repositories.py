import io
from abc import abstractmethod
from pathlib import Path

from ....common.domain import ports as common_ports


class AbstractFileDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def save(self, bytes: io.BytesIO, file_name: str) -> Path:
        """
        :param: File as bytes.
        :raises Path where file is saved.
        """
        pass
