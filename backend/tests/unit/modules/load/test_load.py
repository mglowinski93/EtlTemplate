from modules.load.domain import commands as domain_commands
from modules.load.domain import ports
from modules.load.services import commands
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
    commands.save(unit_of_work=test_data_unit_of_work, command=domain_commands.SaveData(output_data=output_data))

    # Then
    assert len(test_data_unit_of_work.data.data) == 1  # type: ignore[attr-defined]
    assert all(
        [
            output_data[0].full_name == test_data_unit_of_work.data.data[0].full_name,  # type: ignore[attr-defined]
            output_data[0].age == test_data_unit_of_work.data.data[0].age,  # type: ignore[attr-defined]
            output_data[0].is_satisfied
            == test_data_unit_of_work.data.data[0].is_satisfied,  # type: ignore[attr-defined]
        ]
    )
