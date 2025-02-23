import backend.modules.extract.services.ports.strategies as ex
from pathlib import Path
import logging
import pandas as pd
from modules.data.domain.value_objects import InputData



class CsvExtract(ex.AbstractExtract):
    """
    See description of parent class to get more details.
    """

    def extract(path_to_file: Path) -> pd.DataFrame:
        #TODO: change into generic "data extracted" etc
        dataset = pd.read_csv(path_to_file)
        return dataset




class ExcelExtract(ex.AbstractExtract):
    """
    See description of parent class to get more details.
    """
    
    def extract(path_to_file: Path) -> pd.DataFrame:
        dataset = pd.read_excel(path_to_file)
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
