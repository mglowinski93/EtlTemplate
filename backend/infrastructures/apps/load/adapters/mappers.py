from modules.load.services import queries as load_queries

from ..models import Data


def map_data_model_to_output_data_dto(
    data: Data,
) -> load_queries.OutputData:
    return load_queries.OutputData(
        full_name=data.data["full_name"],
        age=data.data["age"],
        is_satisfied=data.data["is_satisfied"],
    )
