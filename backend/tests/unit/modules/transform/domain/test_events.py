from modules.common.domain import events as common_events
from modules.transform.domain import events


def test_data_transformed_event_is_domain_event_type():
    assert issubclass(events.DataTransformed, common_events.DomainEvent)
    assert events.DataTransformed.__dataclass_params__.frozen
