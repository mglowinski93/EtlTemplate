from abc import abstractmethod
from pathlib import Path

from ....common.domain import ports as common_ports


class AbstractFileDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def save(self, file: bytes, file_name: str) -> Path:
        """
        :param file: File to extract data.
        :param file_name: File name to save file with.

        :return: Path to the saved file.
        """

        pass
