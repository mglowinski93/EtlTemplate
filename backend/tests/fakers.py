from modules.common import pagination as pagination_dtos
from modules.load.domain import ports, value_objects
from modules.load.services import queries
from modules.load.services.queries import ports as query_ports
from modules.transform.domain import value_objects as transform_value_objects
import random
import string
from dataclasses import asdict
from datetime import datetime
 
# todo add function to return dictionary data to save 
# return generate random values for transformdata properties 

def fake_transformed_data() -> dict:
    return asdict(transform_value_objects.TransformedData(fake_name(10), fake_age(), fake_is_satisfied()))


def fake_name(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def fake_age():
    return random.randint(0,100)

def fake_is_satisfied():
    return bool(random.getrandbits(1))

def fake_file_name(length = 10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def fake_timestamp():
    return datetime.now()
