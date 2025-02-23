from dataclasses import dataclass

import pandera as pa
from pandera.typing import Series


class InputData(pa.DataFrameModel):
    name: str
    surname: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool


@dataclass
class OutputData:
    full_name: str
    age: int
    is_satisfied: bool
