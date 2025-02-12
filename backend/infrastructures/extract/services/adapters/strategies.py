import backend.modules.extract.services.ports.strategies  as ex
from pathlib import Path
import logging
import pandas as pd

logger = logging.getLogger(_name_)

class ExtractCsvStrategy(ex.ExtractStrategy):
    def extract(path_to_file: Path):
        logger.info("loading csv...")
        return pd.read_csv(path_to_file)


class ExtractExcelStrategy(ex.ExtractStrategy):
    def extract(path_to_file: Path):
        logger.info("loading excel...")  
        return pd.read_excel(path_to_file)


class ExtractPdfStrategy(ex.ExtractStrategy):
    def extract(path_to_file: Path):
        raise NotImplementedError("PDF not implemented yet")


supported_extensions = {
    ".csv": ExtractCsvStrategy(),
    ".xls": ExtractExcelStrategy(),
    ".xlsx": ExtractExcelStrategy(),
    ".pdf": ExtractPdfStrategy()
}
