from dataclasses import dataclass

from ...common.domain import events as common_events
from ..domain import value_objects as domain_value_objects


@dataclass(frozen=True)
class DataTransformed(common_events.DomainEvent):
    output_data: domain_value_objects.OutputData
