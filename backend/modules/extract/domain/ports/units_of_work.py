from abc import ABC

from ....common.domain import ports as common_ports
from .repositories import AbstractExtractDomainRepository, AbstractFileDomainRepository


class AbstractExtractUnitOfWork(common_ports.AbstractUnitOfWork, ABC):
    file: AbstractFileDomainRepository
    extract: AbstractExtractDomainRepository
