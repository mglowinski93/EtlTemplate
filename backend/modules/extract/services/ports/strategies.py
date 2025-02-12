from abc import ABC, abstractmethod
import logging


logger = logging.getLogger(_name_)

class ExtractStrategy(ABC):
    @abstractmethod
    def extract(path_to_file: str):
        pass



