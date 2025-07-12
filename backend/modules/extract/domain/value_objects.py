from dataclasses import dataclass
from datetime import datetime

import pandera as pa

from ...common import ids as common_ids


class FileId(common_ids.Uuid):
    pass


class InputData(pa.DataFrameModel):
    name: str
    surname: str
    age: int = pa.Field(ge=0)
    is_satisfied: bool


@dataclass(frozen=True)
class ExtractHistory:
    input_file_name: str
    saved_file_name: str
    timestamp: datetime
