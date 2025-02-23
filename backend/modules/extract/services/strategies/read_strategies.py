from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class AbstractRead(ABC):
    @abstractmethod
    def read(path_to_file: Path) -> pd.DataFrame:
        """
        :param path_to_file: Path to a file containing data.

        :return: Extracted data in DataFrame format.
        """

        pass


class CsvRead(AbstractRead):
    """
    See description of parent class to get more details.
    """

    def read(path_to_file: Path) -> pd.DataFrame:
        return pd.read_csv(path_to_file)


class ExcelRead(AbstractRead):
    """
    See description of parent class to get more details.
    """

    def read(path_to_file: Path) -> pd.DataFrame:
        return pd.read_excel(path_to_file)


class PdfRead(AbstractRead):
    """
    See description of parent class to get more details.
    """

    def read(path_to_file: Path) -> pd.DataFrame:
        raise NotImplementedError("PDF not implemented yet.")


def choose_strategy(file_extension: str) -> AbstractRead:
    return supported_extensions.get(file_extension)


supported_extensions = {
    ".csv": CsvRead,
    ".xls": ExcelRead,
    ".xlsx": ExcelRead,
    ".pdf": PdfRead,
}
