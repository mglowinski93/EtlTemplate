from abc import ABC, abstractmethod
import logging
from pathlib import Path
from ....data.domain import value_objects as data_value_objects


logger = logging.getLogger(_name_)




class AbstractExtract(ABC):
    @abstractmethod
    def extract(path_to_file: Path) -> data_value_objects.InputData:
        """
        :param path_to_file: Path to a file containing data.

        :return: Data extracted from source file.
        """

        pass
