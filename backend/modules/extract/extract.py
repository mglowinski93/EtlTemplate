from abc import ABC, abstractmethod
import pandas as pd

class ExtractStrategy(ABC):
    @abstractmethod    
    def extract(path_to_file: str):
        pass

class ExtractCsvStrategy(ExtractStrategy):
 
    def extract(path_to_file: str):
        print("loading csv...")
        return pd.read_csv(path_to_file)

class ExtractExcelStrategy(ExtractStrategy):

    def extract(path_to_file: str):
        print("loading excel...")
        return pd.read_excel(path_to_file)

class ExtractPdfStrategy(ExtractStrategy):
 
    def extract(path_to_file: str):
        raise NotImplementedError("PDF not implemented yet")

class ExtractContext():
    def __init__(self, strategy: ExtractStrategy):
        self.strategy = strategy

    def chooseStrategy(self, strategy: ExtractStrategy):
        self.strategy = strategy

    def extract(self, path_to_file: str) -> pd.DataFrame:
        return self.strategy.extract(path_to_file)
