from pathlib import Path

import pandas as pd

from modules.load.services import queries as load_queries
from modules.transform.domain import commands as domain_commands
from modules.transform.services.commands import commands as service_commands


def test_transformed_data_contains_fullname_column():
    # Given
    test_dataset_size = 10
    input_df = pd.read_csv(Path(__file__).parent / "resources" / "correct_input.csv")
    command = domain_commands.TransformData(input_df)

    # When
    result: list[load_queries.OutputData] = service_commands.transform(command)

    # Then
    assert len(result) == test_dataset_size
    assert result.count(load_queries.OutputData("Jessica Barnes", 58, False)) == 1
