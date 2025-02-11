from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path
import pandas as pd
from typing import Self

import modules.extract.extract as extract


class EtlHandler(ABC):
    def __init__(self, next_handler: Self|None = None):
        self.next_handler = next_handler

    @abstractmethod
    def process(self, data: pd.DataFrame):
        pass

    def next(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.next_handler.process() if self.next_handler != None else data
