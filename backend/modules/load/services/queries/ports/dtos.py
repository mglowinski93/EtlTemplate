from dataclasses import dataclass
from datetime import datetime

from .....common.ordering import Ordering


@dataclass
class DataFilters:
    age: int | None = None
    is_satisfied: bool | None = None
    timestamp_from: datetime | None = None
    timestamp_to: datetime | None = None


@dataclass
class DataOrdering:
    age: Ordering | None = None
    timestamp: Ordering | None = None
