from dataclasses import dataclass

from ...data.domain import value_objects as data_value_objects
from ...data.domain.events import DomainEvent


# TODO: discuss what kind of information we want to pass here.  Probably there should be some kind of unique ID of transformed, output dataset. For now data model is used as Event content.
@dataclass(frozen=True)
class DataTransformed(DomainEvent):
    output_data: data_value_objects.OutputData
