from dataclasses import dataclass

from ...common.domain import events as common_events
from ...load.services import queries as load_queries


@dataclass(frozen=True)
class DataTransformed(common_events.DomainEvent):
    output_data: load_queries.OutputData
