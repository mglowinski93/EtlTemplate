from dataclasses import dataclass

from ...data.domain.events import DomainEvent


# TODO: discuss what kind of information we want to pass here. Probably there should be some kind of unique ID of the saved dataset.
@dataclass(frozen=True)
class DataSaved(DomainEvent):
    id: str
