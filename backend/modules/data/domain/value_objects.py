import pandera as pa
from pandera.typing import Series


class InputData(pa.SchemaModel):
    name: Series[str]
    surname: Series[str]
    age: Series[int] = pa.Field(ge=0)
    is_satisfied: Series[bool]


class OutputData(pa.SchemaModel):
    full_name: Series[str]
    age: Series[int] = pa.Field(ge=0)
    is_satisfied: Series[bool]
