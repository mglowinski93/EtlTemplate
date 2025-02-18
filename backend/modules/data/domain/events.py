from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEvent(ABC):
    pass
