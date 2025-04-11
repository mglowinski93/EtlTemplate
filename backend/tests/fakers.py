from modules.common import pagination as pagination_dtos
from modules.load.domain import ports, value_objects
from modules.load.services import queries
from modules.load.services.queries import ports as query_ports
from modules.transform.domain import value_objects as transform_value_objects


 
# todo add function to return dictionary data to save 
# return generate random values for transformdata properties 

def fake_transformed_data() -> transform_value_objects.TransformedData:
    return transform_value_objects.TransformedData("abc", 2, True)
    
    pass
    