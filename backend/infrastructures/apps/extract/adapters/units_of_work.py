from modules.extract.domain.ports import units_of_work

from ...common.adapters import units_of_work as common_units_of_work
from .repositories import DjangoExtractDomainRepository, DjangoFileDomainRepository


class DjangoExtractUnitOfWork(
    common_units_of_work.DjangoUnitOfWork, units_of_work.AbstractExtractUnitOfWork
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
