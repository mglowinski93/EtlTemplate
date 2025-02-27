from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass
