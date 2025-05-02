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
        return pd.concat(
            pd.ExcelFile(BytesIO(file)).parse(None).values(), ignore_index=True
        )


def choose_strategy(file_extension: str) -> type[AbstractExtraction]:
    try:
        return {
            ".csv": CsvExtraction,
            ".xls": ExcelExtraction,
            ".xlsx": ExcelExtraction,
        }[file_extension]
    except KeyError as err:
        raise FileExtensionNotSupportedError(
            message=f"Data format '{file_extension}' is not supported.",
            file_extension=file_extension,
        ) from err
