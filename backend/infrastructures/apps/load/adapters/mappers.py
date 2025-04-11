from modules.load.domain import value_objects
from modules.load.services import queries
from modules.transform.domain import value_objects as transform_value_objects

from ..models import Data


def map_transformed_data_to_data_field(
    data: transform_value_objects.TransformedData,
) -> dict:
    return {
        "full_name": data.full_name,
        "age": data.age,
        "is_satisfied": data.is_satisfied,
    }


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
        timestamp=data.created_at,
    )
