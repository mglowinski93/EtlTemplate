import backend.modules.extract.services.ports.strategies as ex
from pathlib import Path
import logging
import pandas as pd
from modules.data.domain.value_objects import InputData


#TODO: move logging into service layer, or even higher on input level.
logger = logging.getLogger(_name_)



class CsvExtract(ex.AbstractExtract):
    """
    See description of parent class to get more details.
    """

    def extract(path_to_file: Path) -> pd.DataFrame:
        #TODO: change into generic "data extracted" etc
        logger.info("Extracting CSV...")
        dataset = pd.read_csv(path_to_file)
        logger.info("CSV extracted.")
        return dataset




class ExcelExtract(ex.AbstractExtract):
    """
    See description of parent class to get more details.
    """
    
    def extract(path_to_file: Path) -> pd.DataFrame:
        logger.info("Extracting excel...")
        dataset = pd.read_excel(path_to_file)
        logger.info("Excel extracted.")
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
