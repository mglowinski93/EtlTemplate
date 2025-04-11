from dataclasses import dataclass


@dataclass(frozen=True)
class TransformedData:
    full_name: str
    age: int
    is_satisfied: bool
