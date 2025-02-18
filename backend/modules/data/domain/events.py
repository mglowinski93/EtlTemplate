from dataclasses import dataclass
from pathlib import Path


class Event:
    pass

#TODO: add event properties later
@dataclass
class DataExtracted(Event):
    pass

@dataclass
class DataTransformed(Event):
    pass

@dataclass
class DataSaved(Event):
    pass
