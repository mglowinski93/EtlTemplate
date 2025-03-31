import pandas as pd

from modules.transform.domain import commands as transform_commands
from modules.transform.domain import value_objects as transform_value_objects
from modules.transform.services.commands import commands as service_commands

from tests import test_const


def test_transformed_data_contains_fullname_column():
    # Given
    test_dataset_size = 10
    input_df = pd.read_csv(test_const.CORRECT_INPUT_CSV)
    command = transform_commands.TransformData(input_df)

    # When
    result: list[transform_value_objects.OutputData] = service_commands.transform(command)

    # Then
    assert len(result) == test_dataset_size
    assert (
        result.count(transform_value_objects.OutputData("Jessica Barnes", 58, False)) == 1
    )
