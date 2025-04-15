from faker import Faker

from ..... import fakers

fake = Faker()


def fake_data_id() -> str:
    return fake.uuid4()


def fake_data(is_satisfied: bool = None) -> dict:  # type: ignore[assignment]
    return {
        "full_name": fakers.fake_full_name(),
        "age": fakers.fake_age(),
        "is_satisfied": fakers.fake_is_satisfied()
        if is_satisfied is None
        else is_satisfied,
    }
