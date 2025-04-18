from modules.extract.domain import ports

from ...common.adapters import units_of_work as common_units_of_work
from .repositories import DjangoExtractDomainRepository, DjangoFileDomainRepository


class DjangoExtractUnitOfWork(
    common_units_of_work.DjangoUnitOfWork, ports.AbstractExtractUnitOfWork
):
    def __init__(self):
        super().__init__(
            [
                common_units_of_work.RepositoryData(
                    "file",
                    DjangoFileDomainRepository,
                ),
                common_units_of_work.RepositoryData(
                    "extract", DjangoExtractDomainRepository
                ),
            ]
        )
