from abc import ABC

from ....common.domain.ports import units_of_work
from .repositories import (
    AbstractDataDomainRepository,
)


class AbstractDataUnitOfWork(units_of_work.AbstractUnitOfWork, ABC):
    data: AbstractDataDomainRepository
