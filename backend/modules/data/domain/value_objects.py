from dataclasses import dataclass

import pandera as pa


class InputData(pa.DataFrameModel):
    name: str
    surname: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool


@dataclass(frozen=True)
class OutputData:
    full_name: str
    age: int
    is_satisfied: bool
