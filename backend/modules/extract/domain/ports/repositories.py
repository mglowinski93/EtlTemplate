from abc import abstractmethod

from ....common.domain import ports as common_ports
from ...domain import value_objects


class AbstractFileDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def save(self, file: bytes, file_name: str) -> str:
        """
        :param file: File to extract data.
        :param file_name: File name to save file with.

        :return: Name of the saved file.
        """

        pass

    @abstractmethod
    def file_exists(self, file_name: str) -> bool:
        """
        :param file_name: File checked.

        :return: True if file exists, otherwise False.
        """

        pass


class AbstractExtractDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def create(self, extract_history: value_objects.ExtractHistory) -> None:
        """
        :param: Data to save.
        """

        pass
