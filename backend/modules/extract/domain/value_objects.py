import pandera as pa

from datetime import datetime
from dataclasses import dataclass

class InputData(pa.DataFrameModel):
    name: str
    surname: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool

@dataclass
class ExtractHistory():
    input_file_name: str
    saved_file_name: str
    timestamp: datetime
