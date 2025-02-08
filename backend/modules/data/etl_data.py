from dataclasses import dataclass


@dataclass(frozen=True)
class EtlEntryData():
    def __init__(self, name : str, surname : str, age : int, is_satisfied : bool):
        self.name = name
        self.surname = surname
        self.age = age
        self.is_satisfied = is_satisfied
