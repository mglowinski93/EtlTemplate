from dataclasses import dataclass
from datetime import datetime
from ..dtos import OutputData
from .....common.ordering import Ordering


@dataclass
class OutputDataFilters:
    age: int | None = None
    is_satisfied: bool | None = None
    timestamp_from: datetime | None = None
    timestamp_to: datetime | None = None


@dataclass
class OutputDataOrdering:
    timestamp: datetime | None = None
