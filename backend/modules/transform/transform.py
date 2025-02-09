from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path
import pandas as pd

import modules.extract.extract as extract

class EtlHandler(ABC):
    def __init__(self, next_handler: Optional["EtlHandler"] = None):
        self.next_handler = next_handler
    
    @abstractmethod
    def process(self, data):
        pass

    def next(self, data: pd.DataFrame):
        return self.next_handler.process() if self.next_handler != None else data

# TODO - add Extractor Handler
class ExtractHandler(EtlHandler):
    def __init__(self, path_to_file: str, next_handler: Optional["EtlHandler"] = None):
        self.path_to_file = path_to_file
        self.next_handler = next_handler

    def process(self, data = None):
        data_file_path = Path(self.path_to_file)
        file_extension = data_file_path.suffix()
        strat = self._chooseStrategy(file_extension)
        extract_context = extract.ExtractContext(strat)
        df = extract_context.extract(self.path_to_file)
        self.next(df)

    def _chooseStrategy(file_extension: str) -> extract.ExtractStrategy:
        if file_extension.lower() == ".csv":
            return extract.ExtractCsvStrategy()
        elif file_extension.lower() in [".xls", ".xlsx"]:
            return extract.ExtractExcelStrategy()
        elif file_extension.lower() in [".pdf"]:
            return extract.ExtractPdfStrategy
        else :
            raise TypeError(file_extension)


# TODO - add Transformation Handler
# TODO - add Persistance Handler
