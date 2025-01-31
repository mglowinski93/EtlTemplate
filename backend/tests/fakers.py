from datetime import datetime

from faker import Faker

from modules.common import time
from modules.transform.domain import value_objects as transform_value_objects

fake = Faker()


def fake_full_name() -> str:
    return f"{fake.first_name()} {fake.last_name()}"


def fake_age() -> int:
    return fake.random_int(1, 100)


def fake_is_satisfied() -> bool:
    return fake.boolean()


def fake_file_name() -> str:
    return fake.file_name()


def fake_timestamp() -> datetime:
    return time.get_current_timestamp()


def fake_transformed_data() -> transform_value_objects.TransformedData:
    return transform_value_objects.TransformedData(
        full_name=fake_full_name(), age=fake_age(), is_satisfied=fake_is_satisfied()
    )


def fake_username() -> str:
    return fake.text(max_nb_chars=20)
