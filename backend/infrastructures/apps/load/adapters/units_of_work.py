from modules.load.domain import ports

from ...common.adapters import units_of_work
from .repositories import DjangoDataDomainRepository


class DjangoDataUnitOfWork(
    units_of_work.DjangoUnitOfWork, ports.AbstractDataUnitOfWork
):
    def __init__(self):
        super().__init__(
            [
                units_of_work.RepositoryData(
                    "data",
                    DjangoDataDomainRepository,
                ),
            ]
        )
