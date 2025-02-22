import pandera as pa
from pandera.typing import Series
from dataclasses import dataclass

@dataclass
class InputData(pa.DataFrameModel):
    name: str
    surname: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool


@dataclass
class OutputData(pa.DataFrameModel):
    full_name: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool
