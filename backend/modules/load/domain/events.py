from dataclasses import dataclass

from ...common.domain import events as common_events
from ...load.services import queries as load_queries


@dataclass(frozen=True)
class DataSaved(common_events.DomainEvent):
    data: load_queries.OutputData
