from abc import ABC, abstractmethod
import logging
from pathlib import Path
import pandas as pd


logger = logging.getLogger(_name_)

"""Abstract base class for defining data extraction strategies.
:param path_to_file: Path to a file containing data

:return: data extracted from source file in form of pandas DataFrame 
"""


class AbstractExtract(ABC):
    @abstractmethod
    def extract(path_to_file: Path) -> pd.DataFrame:
        pass
