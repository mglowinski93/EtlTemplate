from abc import ABC, abstractmethod
import pandas as pd


class TransformService(ABC):
    @abstractmethod
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        pass
