from faker import Faker

fake = Faker()


def fake_data_id() -> str:
    return fake.uuid4()
