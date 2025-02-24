from pathlib import Path

import pandas as pd

import backend.modules.extract.services.ports.strategies as ex


class CsvExtract(ex.AbstractExtract):
    """
    See description of parent class to get more details.
    """

    def extract(path_to_file: Path) -> pd.DataFrame:
        return pd.read_csv(path_to_file)


class ExcelExtract(ex.AbstractExtract):
    """
    See description of parent class to get more details.
    """

    def extract(path_to_file: Path) -> pd.DataFrame:
        return pd.read_excel(path_to_file)


class PdfExtract(ex.AbstractExtract):
    """
    See description of parent class to get more details.
    """

    def extract(path_to_file: Path) -> pd.DataFrame:
        raise NotImplementedError("PDF not implemented yet.")


supported_extensions = {
    ".csv": CsvExtract,
    ".xls": ExcelExtract,
    ".xlsx": ExcelExtract,
    ".pdf": PdfExtract,
}
