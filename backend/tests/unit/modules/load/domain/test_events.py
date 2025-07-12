from modules.common.domain import events as common_events
from modules.load.domain import events


def test_data_saved_event_is_domain_event_type():
    assert issubclass(events.DataSaved, common_events.DomainEvent)
    assert events.DataSaved.__dataclass_params__.frozen
