from abc import ABC, abstractmethod
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(_name_)

class ExtractStrategy(ABC):
    @abstractmethod
    def extract(path_to_file: str):
        pass



