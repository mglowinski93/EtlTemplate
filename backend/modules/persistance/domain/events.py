from dataclasses import dataclass

from ...common.domain import events as common_events
from ...data.domain import value_objects as data_value_objects


@dataclass(frozen=True)
class DataSaved(common_events.DomainEvent):
    data: data_value_objects.OutputData
