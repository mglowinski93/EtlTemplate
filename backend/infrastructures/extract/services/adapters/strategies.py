import backend.modules.extract.services.ports.strategies as ex
from pathlib import Path
import logging
import pandas as pd


logger = logging.getLogger(_name_)

"""
See description of parent class to get more details.
"""


class CsvExtract(ex.AbstractExtract):
    def extract(path_to_file: Path) -> pd.DataFrame:
        logger.info("Extracting csv...")
        return pd.read_csv(path_to_file)


"""
See description of parent class to get more details.
"""


class ExcelExtract(ex.AbstractExtract):
    def extract(path_to_file: Path) -> pd.DataFrame:
        logger.info("Extracting excel...")
        return pd.read_excel(path_to_file)


"""
See description of parent class to get more details.
"""


class PdfExtract(ex.AbstractExtract):
    def extract(path_to_file: Path) -> pd.DataFrame:
        raise NotImplementedError("PDF not implemented yet")


supported_extensions = {
    ".csv": CsvExtract(),
    ".xls": ExcelExtract(),
    ".xlsx": ExcelExtract(),
    ".pdf": PdfExtract(),
}
