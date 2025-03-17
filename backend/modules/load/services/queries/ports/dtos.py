from dataclasses import dataclass

from .....data.domain.value_objects import OutputData
from .....common.ordering import Ordering


@dataclass
class OutputDataFilters:
    ids: list[OutputData] | None = None
    full_name: str | None = None
    age: int | None = None
    is_satisfied: bool | None = None


@dataclass
class OutputDataOrdering:
    full_name: Ordering | None = None
    age: Ordering | None = None
    is_satisfied: Ordering | None = None
