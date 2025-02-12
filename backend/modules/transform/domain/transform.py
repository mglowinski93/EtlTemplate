import pandas as pd
from services.services import TransformService

# for now this Transformer doesn't do anything yet
class TransformationHandler:

    def __init__(self, ts: TransformService):
        self.transformation_service = ts


    def process(self, df: pd.DataFrame):
        result_df = self.transformation_service.transform(df)
        return self.next(result_df)
