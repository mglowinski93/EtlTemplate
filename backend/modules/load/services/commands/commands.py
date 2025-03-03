from ...domain import commands as domain_commands
from ...domain.ports import units_of_work


def save(
    command: domain_commands.SaveData,
    unit_of_work: units_of_work.AbstractDataUnitOfWork,
):
    with unit_of_work:
        unit_of_work.data.create(command.output_data)
