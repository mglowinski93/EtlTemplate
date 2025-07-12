from modules.common.domain import events as common_events
from modules.extract.domain import events


def test_data_extracted_event_is_domain_event_type():
    assert issubclass(events.DataExtracted, common_events.DomainEvent)
    assert events.DataExtracted.__dataclass_params__.frozen
