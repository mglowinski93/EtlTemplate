import random
import string
from dataclasses import asdict
from datetime import datetime

from modules.transform.domain import value_objects as transform_value_objects


def fake_name(length=10):
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )


def fake_age():
    return random.randint(0, 100)


def fake_is_satisfied():
    return bool(random.getrandbits(1))


def fake_file_name(length=10):
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )


def fake_timestamp():
    return datetime.now()


def fake_transformed_data() -> transform_value_objects.TransformedData:
    return transform_value_objects.TransformedData(
        fake_name(10), fake_age(), fake_is_satisfied()
    )
