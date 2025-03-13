from ...load import models as orm_models
from modules.data.domain import value_objects as data_value_objects

def map_outputdata_model_to_output_dto(output_data: orm_models.OutputData):
    return data_value_objects.OutputData(full_name=output_data.full_name, age=output_data.age, is_satisfied=output_data.is_satisfied)
