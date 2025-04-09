from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from django.db import transaction

from modules.common.domain import ports


@dataclass(frozen=True)
class RepositoryData:
    name: str
    repository: Type[ports.AbstractDomainRepository]


class DjangoUnitOfWork(ports.AbstractUnitOfWork):
    def __init__(self, repositories: list[RepositoryData]):
        for repository in repositories:
            setattr(self, repository.name, repository.repository())

    def __enter__(self) -> DjangoUnitOfWork:
        transaction.set_autocommit(False)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            transaction.set_autocommit(True)

    def commit(self) -> None:
        transaction.commit()

    def rollback(self) -> None:
        transaction.rollback()
