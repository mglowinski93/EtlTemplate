from dataclasses import dataclass

from ...common.domain import events as common_events
from ..domain.value_objects import TransformedData


@dataclass(frozen=True)
class DataTransformed(common_events.DomainEvent):
    data: TransformedData
