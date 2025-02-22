from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from ....data.domain import value_objects as data_value_objects


class AbstractExtract(ABC):
    @abstractmethod
    def extract(path_to_file: Path) -> pd.DataFrame:
        """
        :param path_to_file: Path to a file containing data.

        :return: Extracted data in DataFrame format.
        """

        pass
