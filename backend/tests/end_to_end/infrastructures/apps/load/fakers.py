from faker import Faker

from ..... import fakers

from modules.load.domain import value_objects

fake = Faker()


def fake_data_id() -> value_objects.DataId:
    return value_objects.DataId.new()

def fake_data(is_satisfied: bool | None = None) -> dict:  # type: ignore[assignment]
    return {
        "full_name": fakers.fake_full_name(),
        "age": fakers.fake_age(),
        "is_satisfied": fakers.fake_is_satisfied()
        if is_satisfied is None
        else is_satisfied,
    }
