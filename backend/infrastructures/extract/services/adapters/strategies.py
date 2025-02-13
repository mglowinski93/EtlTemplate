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
        logger.info("Extracting CSV...")
        dataset = pd.read_csv(path_to_file)
        logger.info("CSV extracted.")
        return dataset

"""
See description of parent class to get more details.
"""


class ExcelExtract(ex.AbstractExtract):
    def extract(path_to_file: Path) -> pd.DataFrame:
        logger.info("Extracting excel...")
        dataset = pd.read_excel(path_to_file)
        logger.info("Excel extracted.")
        return pd.read_excel(path_to_file)


"""
See description of parent class to get more details.
"""


class PdfExtract(ex.AbstractExtract):
    def extract(path_to_file: Path) -> pd.DataFrame:
        raise NotImplementedError("PDF not implemented yet.")


supported_extensions = {
    ".csv": CsvExtract(),
    ".xls": ExcelExtract(),
    ".xlsx": ExcelExtract(),
    ".pdf": PdfExtract(),
}
