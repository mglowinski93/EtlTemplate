from abc import ABC, abstractmethod
from typing import Optional

class EtlHandler(ABC):
    def __init__(self, next_handler: Optional["EtlHandler"] = None):
        self.next_handler = next_handler
    
    @abstractmethod
    def process(self, data):
        pass

    def next(self, data):
        return self.next_handler.process() if self.next_handler != None else data

# TODO - add Extractor Handler
# TODO - add Transformation Handler
# TODO - add Persistance Handler
