import modules.transform.transform as transform
import pandas as pd

class TransformationHandler():
    def process(self, df: pd.DataFrame):
        if df == None:
            raise ValueError("Input DataFrame doesn't exist")
        return self.next(df)
