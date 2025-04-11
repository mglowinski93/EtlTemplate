from modules.common import pagination as pagination_dtos
from modules.load.domain import ports, value_objects
from modules.load.services import queries
from modules.load.services.queries import ports as query_ports
from modules.transform.domain import value_objects as transform_value_objects
import random
import string
from dataclasses import asdict
 
# todo add function to return dictionary data to save 
# return generate random values for transformdata properties 

def fake_transformed_data() -> dict:
    return asdict(transform_value_objects.TransformedData(_generate_random_strings(10), _generate_random_int(), _generate_random_bool()))


def _generate_random_strings(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def _generate_random_int():
    return random.randint(0,100)

def _generate_random_bool():
    return bool(random.getrandbits(1))
