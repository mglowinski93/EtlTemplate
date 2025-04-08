from modules.load.services import queries

from ..models import Data
from modules.load.domain import value_objects

def map_data_model_to_output_data_dto(
    data: Data,
) -> queries.OutputData:
    return queries.OutputData(
        id=value_objects.DataId.from_hex(data.id.hex),
        full_name=data.data["full_name"],
        age=data.data["age"],
        is_satisfied=data.data["is_satisfied"],
    )

def map_data_model_to_detailed_output_data_dto(
    data: Data,
) -> queries.DetailedOutputData:
    return queries.DetailedOutputData(
        id=value_objects.DataId.from_hex(data.id.hex),
        full_name=data.data["full_name"],
        age=data.data["age"],
        is_satisfied=data.data["is_satisfied"],
        timestamp=data.created_at
    )
