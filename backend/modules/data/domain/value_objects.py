import pandera as pa
from pandera.typing import DataFrame 

#TODO test it if dataframe still works
class InputData(pa.DataFrameModel):
    name: str
    surname: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool
