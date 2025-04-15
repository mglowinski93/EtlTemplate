from faker import Faker

from ..... import fakers

fake = Faker()


def fake_data_id() -> str:
    return fake.uuid4()

def fake_data(age: int = 0, is_satisfied: bool = None) -> dict:
    return {
            "full_name" : fakers.fake_full_name(),
            "age" : fakers.fake_age() if age == 0 else age,
            "is_satisfied" : fakers.fake_is_satisfied() if is_satisfied is None else is_satisfied
        }
    