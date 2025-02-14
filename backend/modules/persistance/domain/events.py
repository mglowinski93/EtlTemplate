from dataclasses import dataclass
from pathlib import Path
from ...common.domain.events import DomainEvent
from ...data.domain import value_objects  as data_value_objects


@dataclass(frozen=True)
class DataPersisted(DomainEvent):
    output_data: data_value_objects. OutputData #TODO : Here we probably should add a unique ID for each data set.
