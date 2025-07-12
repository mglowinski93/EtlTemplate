from abc import ABC

from ....common.domain import ports as common_ports
from .repositories import AbstractDataDomainRepository


class AbstractDataUnitOfWork(common_ports.AbstractUnitOfWork, ABC):
    data: AbstractDataDomainRepository
