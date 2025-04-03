import pandas as pd

from modules.transform.domain import commands as transform_commands
from modules.transform.domain import value_objects as transform_value_objects
from modules.transform.services.commands import commands as service_commands
from tests import test_const


def test_transformed_data_contains_fullname_column():
    # Given
    test_dataset_size = 10
    input_df = pd.read_csv(test_const.TRANSFORM_CORRECT_INPUT_CSV)
    command = transform_commands.TransformData(input_df)

    # When
    result: list[transform_value_objects.OutputData] = service_commands.transform(
        command
    )

    # Then
    assert len(result) == test_dataset_size
    assert (
        result.count(
            transform_value_objects.OutputData(
                full_name="Jessica Barnes", age=58, is_satisfied=False
            )
        )
        == 1
    )
