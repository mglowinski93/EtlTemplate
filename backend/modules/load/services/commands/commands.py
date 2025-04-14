from ...domain.commands import SaveData
from ...domain.ports.units_of_work import AbstractDataUnitOfWork


def save(
    unit_of_work: AbstractDataUnitOfWork,
    command: SaveData,
):
    with unit_of_work:
        unit_of_work.data.create(command.data)
