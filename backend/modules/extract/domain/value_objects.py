from dataclasses import dataclass
from datetime import datetime

import pandera as pa


class InputData(pa.DataFrameModel):
    name: str
    surname: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool


@dataclass
class ExtractHistory:
    input_file_name: str
    saved_file_name: str
    timestamp: datetime
