from faker import Faker

from modules.load.domain import value_objects

from ..... import consts, fakers

fake = Faker()


def fake_data_id() -> value_objects.DataId:
    return value_objects.DataId.new()


def fake_data(is_satisfied: bool | None = None) -> dict:
    return {
        "full_name": fakers.fake_full_name(),
        "age": fakers.fake_age(),
        "is_satisfied": fakers.fake_is_satisfied()
        if is_satisfied is None
        else is_satisfied,
    }


def fake_data_form(
    full_name: str | None = None,
    age: int | None = None,
    is_satisfied: bool | None = None,
) -> dict:
    return {
        consts.EXPORT_FORM_DATA_NAME: {
            "full_name": fakers.fake_full_name() if full_name is None else full_name,
            "age": fakers.fake_age() if age is None else age,
            "is_satisfied": fakers.fake_is_satisfied()
            if is_satisfied is None
            else is_satisfied,
        }
    }
