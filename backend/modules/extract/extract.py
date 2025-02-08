from pathlib import Path
from typing import Optional

import pandas as pd

class FileExtractor:
    def __init__(self):
        pass

    def extract_file(self, file_path: str):
        data_file_path = Path(file_path)
        file_extension = data_file_path.suffix
        df = None
        if file_extension.lower() == ".csv":
            print("loading csv...")
            df = pd.read_csv(file_path)
        elif file_extension.lower() in [".xls", ".xlsx"]:
            print("loading excel...")
            df = pd.read_excel(file_path)
        else :
            raise TypeError(file_extension)
        return df
    