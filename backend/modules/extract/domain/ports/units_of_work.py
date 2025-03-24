from abc import ABC

from ....common.domain.ports import units_of_work
from .repositories import (
    AbstractFileDomainRepository,
)


class AbstractFileUnitOfWork(units_of_work.AbstractUnitOfWork, ABC):
    file: AbstractFileDomainRepository
