import pandera as pa


class InputData(pa.DataFrameModel):
    name: str
    surname: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool
