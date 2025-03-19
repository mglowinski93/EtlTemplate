from modules.load.services import queries as load_queries

from ..models import Data


def map_outputdata_model_to_output_dto(
    output_data: Data,
) -> load_queries.OutputData:
    return load_queries.OutputData(
        full_name=output_data.data["full_name"],
        age=output_data.data["age"],
        is_satisfied=output_data.data["is_satisfied"],
    )
