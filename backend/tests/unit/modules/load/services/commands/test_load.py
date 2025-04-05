from modules.load.domain import commands as domain_commands
from modules.load.domain import ports
from modules.load.services.commands import commands
from modules.transform.domain import value_objects as transform_value_objects


def test_data_saved_successfully(
    test_data_unit_of_work: ports.AbstractDataUnitOfWork,
):
    # Given
    output_data = [
        transform_value_objects.OutputData(
            full_name="Jessica Barnes", age=58, is_satisfied=False
        ),
    ]

    # When
    commands.save(
        unit_of_work=test_data_unit_of_work,
        command=domain_commands.SaveData(output_data=output_data),
    )

    # Then
    assert len(test_data_unit_of_work.data.data) == 1  # type: ignore[attr-defined]
    assert all(
        given_data.full_name == result.full_name
        and given_data.age == result.age
        and given_data.is_satisfied == result.is_satisfied
        for given_data, result in zip(output_data, test_data_unit_of_work.data.list())  # type: ignore[attr-defined]
    )
