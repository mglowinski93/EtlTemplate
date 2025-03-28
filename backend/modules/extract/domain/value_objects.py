import pandera as pa
from datetime import datetime


class InputData(pa.DataFrameModel):
    name: str
    surname: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool

class ExtractHistory():
    input_file_name: str
    saved_file_name: str
    timestamp: datetime
