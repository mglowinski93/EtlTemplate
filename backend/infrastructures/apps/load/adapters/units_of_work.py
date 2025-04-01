from modules.load.domain.ports import units_of_work as domain_units_of_work

from ...common.adapters import units_of_work
from .repositories import DjangoDataDomainRepository


class DjangoDataUnitOfWork(
    units_of_work.DjangoUnitOfWork, domain_units_of_work.AbstractDataUnitOfWork
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
