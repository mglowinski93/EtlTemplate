from dataclasses import dataclass

from ...common.domain import events as common_events
from ...transform.domain import value_objects as transform_value_objects


@dataclass(frozen=True)
class DataSaved(common_events.DomainEvent):
    data: transform_value_objects.TransformedData
