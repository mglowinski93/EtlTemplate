import backend.modules.extract.services.ports.strategies  as ex
from backend.modules.data.domain.exceptions import FileTypeNotSupportedErrod
import pandas as pd
import infrastructures.extract.strategies as strat

supported_extensions = {
    ".csv": strat.ExtractCsvStrategy(),
    ".xls": strat.ExtractExcelStrategy(),
    ".xlsx": strat.ExtractExcelStrategy(),
    ".pdf": strat.ExtractPdfStrategy()
}

class ExtractManager:
    #TODO: change file_path to string and check if file exists. if not - raise error
    def extract(self, file_path: str) -> pd.DataFrame:
        file_extension = file_path.suffix()
        chosen_strat = self.chooseStrategy(file_extension)
        df = chosen_strat.extract(self.path_to_file)
       

    def chooseStrategy(file_extension: str) -> ex.ExtractStrategy:
            strat = supported_extensions.get(file_extension)
            if strat == None:
                raise FileTypeNotSupportedErrod(file_extension) 



