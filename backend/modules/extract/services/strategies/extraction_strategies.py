from abc import ABC, abstractmethod
from django.conf import settings
from pathlib import Path

import pandas as pd

from ...domain.exceptions import FileExtensionNotSupportedError


class AbstractExtraction(ABC):
    @abstractmethod
    def read(self, file_name: str) -> pd.DataFrame:
        """
        :param file_name: File name containing data.

        :return: Extracted data in DataFrame format.
        """

        pass


class CsvExtraction(AbstractExtraction):
    """
    See description of parent class to get more details.
    """

    def read(self, file_name: str) -> pd.DataFrame:
        return pd.read_csv(Path(settings.MEDIA_ROOT) / file_name)


class ExcelExtraction(AbstractExtraction):
    """
    See description of parent class to get more details.
    """

    def read(self, file_name: str) -> pd.DataFrame:
        return pd.read_excel(Path(settings.MEDIA_ROOT) / file_name)


def choose_strategy(file_extension: str) -> type[AbstractExtraction]:
    strategy = SUPPORTED_EXTENSIONS.get(file_extension)
    if strategy is None:
        raise FileExtensionNotSupportedError(
            message="Data format '%s' is not supported.", file_extension=file_extension
        )
    return strategy


SUPPORTED_EXTENSIONS = {
    ".csv": CsvExtraction,
    ".xls": ExcelExtraction,
    ".xlsx": ExcelExtraction,
}
