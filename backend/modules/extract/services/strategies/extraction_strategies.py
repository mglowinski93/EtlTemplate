from abc import ABC, abstractmethod
from io import BytesIO

import pandas as pd

from ...domain.exceptions import FileExtensionNotSupportedError


class AbstractExtraction(ABC):
    @abstractmethod
    def read(self, file: bytes) -> pd.DataFrame:
        """
        :param file: File containing data.

        :return: Extracted data in DataFrame format.
        """

        pass


class CsvExtraction(AbstractExtraction):
    """
    See description of parent class to get more details.
    """

    def read(self, file: bytes) -> pd.DataFrame:
        return pd.read_csv(BytesIO(file))


class ExcelExtraction(AbstractExtraction):
    """
    See description of parent class to get more details.
    """

    def read(self, file: bytes) -> pd.DataFrame:
        return pd.ExcelFile(file)


def choose_strategy(file_extension: str) -> type[AbstractExtraction]:
    if file_extension not in SUPPORTED_EXTENSIONS:
        raise FileExtensionNotSupportedError(
            message="Data format '%s' is not supported.", file_extension=file_extension
        )
    return SUPPORTED_EXTENSIONS[file_extension]


SUPPORTED_EXTENSIONS = {
    ".csv": CsvExtraction,
    ".xls": ExcelExtraction,
    ".xlsx": ExcelExtraction,
}
