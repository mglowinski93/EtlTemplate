from dataclasses import dataclass


@dataclass(frozen=True)
class OutputData:
    full_name: str
    age: int
    is_satisfied: bool
