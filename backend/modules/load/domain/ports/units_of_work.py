from abc import ABC

from ....common.domain.ports import units_of_work
from .repositories import (
    AbstractLoadRepository,
)


class AbstractLoadUnitOfWork(units_of_work.AbstractUnitOfWork, ABC):
    repository: AbstractLoadRepository
