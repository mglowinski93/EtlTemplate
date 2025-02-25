from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from ....common.domain.exceptions import FileDataFormatNotSupportedException


class AbstractExtraction(ABC):
    @abstractmethod
    def read(self, path_to_file: Path) -> pd.DataFrame:
        """
        :param path_to_file: Path to a file containing data.

        :return: Extracted data in DataFrame format.
        """

        pass


class CsvExtraction(AbstractExtraction):
    """
    See description of parent class to get more details.
    """

    def read(self, path_to_file: Path) -> pd.DataFrame:
        return pd.read_csv(path_to_file)


class ExcelExtraction(AbstractExtraction):
    """
    See description of parent class to get more details.
    """

    def read(self, path_to_file: Path) -> pd.DataFrame:
        return pd.read_excel(path_to_file)


def choose_strategy(file_extension: str) -> type[AbstractExtraction]:
    strat = SUPPORTED_EXTENSIONS.get(file_extension)
    if strat is None:
        raise FileDataFormatNotSupportedException(
            f"Data format {file_extension} is not supported."
        )
    return strat


SUPPORTED_EXTENSIONS = {
    ".csv": CsvExtraction,
    ".xls": ExcelExtraction,
    ".xlsx": ExcelExtraction,
}
