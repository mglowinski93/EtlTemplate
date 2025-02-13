import pandas as pd
from services.services import TransformService


# for now this Transformer doesn't do anything yet
class TransformManager:
    def __init__(self, transform_service: TransformService):
        self.transform_service = transform_service

    def process(self, df: pd.DataFrame):
        result_df = self.transform_service.transform(df)
        return self.next(result_df)
