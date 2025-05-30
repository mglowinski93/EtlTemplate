import pandas as pd

from modules.transform.domain import commands as transform_commands
from modules.transform.domain import value_objects as transform_value_objects
from modules.transform.services.commands import commands as service_commands

from ...... import consts


def test_transformed_data_contains_fullname_column():
    # Given
    test_dataset_size = 10
    command = transform_commands.TransformData(
        pd.read_csv(consts.TRANSFORM_CORRECT_INPUT_CSV)
    )

    # When
    result: list[transform_value_objects.TransformedData] = service_commands.transform(
        command
    )

    # Then
    assert len(result) == test_dataset_size
    assert (
        result.count(
            transform_value_objects.TransformedData(
                full_name="Jessica Barnes", age=58, is_satisfied=False
            )
        )
        == 1
    )
