from dataclasses import dataclass

from ...common.domain import events as common_events
from ...data.domain import value_objects as data_value_objects


@dataclass(frozen=True)
class DataTransformed(common_events.DomainEvent):
    output_data: data_value_objects.OutputData
