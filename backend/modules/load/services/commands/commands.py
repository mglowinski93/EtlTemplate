from ...domain import commands as domain_commands
from ...domain.ports import units_of_work


def load(command: domain_commands.LoadData, uow: units_of_work.AbstractLoadUnitOfWork):
    with uow:
        uow.repository.load(command.output_data)
        uow.commit()
