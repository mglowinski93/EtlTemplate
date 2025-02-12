import pandera as pa
from pandera.typing import Series


class EtlEntryData(pa.SchemaModel):
    name: Series[str]
    surname: Series[str]
    age: Series[int] = pa.Field(ge=0)
    is_satisfied: Series[bool]


class EtlOutputData(pa.SchemaModel):
    name_surname: Series[str]
    age: Series[int] = pa.Field(ge=0)
    is_satisfied: Series[bool]
