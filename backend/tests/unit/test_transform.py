from pathlib import Path

import pandas as pd

from modules.transform.domain import commands as domain_commands
from modules.transform.services.commands import commands as service_commands


def test_transformed_data_contains_fullname_column():
    # Given
    input_df = pd.read_csv(Path(__file__).parent / "resources" / "correct_input.csv")
    command = domain_commands.TransformData(input_df)

    # When
    result: pd.DataFrame = service_commands.transform(command)

    # Then
    assert "full_name" in result.columns
    assert "Jessica Barnes" in result["full_name"].values
    assert result.shape[0] == 10
