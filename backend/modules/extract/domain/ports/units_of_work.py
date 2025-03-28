from abc import ABC

from ....common.domain.ports import units_of_work
from .repositories import (
    AbstractFileDomainRepository, 
    AbstractExtractDomainRepository,
)


class AbstractExtractUnitOfWork(units_of_work.AbstractUnitOfWork, ABC):
    file: AbstractFileDomainRepository
    extract: AbstractExtractDomainRepository
