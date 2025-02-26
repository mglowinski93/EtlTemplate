from pathlib import Path

import pandas as pd

from modules.data.domain import value_objects as data_value_objects
from modules.transform.domain import commands as domain_commands
from modules.transform.services.commands import commands as service_commands


def test_transformed_data_contains_fullname_column():
    # Given
    input_df = pd.read_csv(Path(__file__).parent / "resources" / "correct_input.csv")
    command = domain_commands.TransformData(input_df)

    # When
    result: list[data_value_objects.OutputData] = service_commands.transform(command)

    # Then
    assert len(result) == TEST_DATASET_SIZE
    assert result.count(data_value_objects.OutputData("Jessica Barnes", 58, False)) == 1

TEST_DATASET_SIZE = 10
