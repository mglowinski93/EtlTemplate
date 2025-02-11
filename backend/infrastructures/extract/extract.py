import modules.extract.extract  as ex
from pathlib import Path
import logging
import pandas as pd
import infrastructures.extract.strategies as strat


class ExtractManager:
    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file

    #TODO: change file_path to string and check if file exists. if now - raise error
    def extract(self, file_path: str) -> pd.DataFrame:
        file_extension = file_path.suffix()
        chosen_strat = self.chooseStrategy(file_extension)
        df = chosen_strat.extract(self.path_to_file)
       

    def chooseStrategy(file_extension: str) -> ex.ExtractStrategy:
        if file_extension.lower() == ".csv":
            return strat.ExtractCsvStrategy()
        elif file_extension.lower() in [".xls", ".xlsx"]:
            return strat.ExtractExcelStrategy()
        elif file_extension.lower() in [".pdf"]:
            return strat.ExtractPdfStrategy
        else:
            raise TypeError(file_extension) #TODO: replace with dedifacted error 



