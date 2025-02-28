from ...domain import commands as domain_commands
from ...domain.ports import units_of_work


def load(command: domain_commands.LoadData, unit_of_work: units_of_work.AbstractLoadUnitOfWork):
    with unit_of_work:
        unit_of_work.repository.load(command.output_data)
        unit_of_work.commit()
