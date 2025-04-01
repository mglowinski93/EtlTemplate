from dataclasses import dataclass

from ...common.domain import events as common_events
from ..domain import value_objects


@dataclass(frozen=True)
class DataTransformed(common_events.DomainEvent):
    output_data: value_objects.OutputData
