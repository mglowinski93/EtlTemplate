import logging
from pprint import pformat
from typing import Any

from django.contrib.auth import get_user_model

from modules.load.services.queries import ports as query_ports 
from modules.data.domain import value_objects as data_value_objects


logger = logging.getLogger(__name__)

class DjangoDataQueryRepository(query_ports.AbstractDataQueryRepository):
    """
    See description of parent class to get more details.
    """
    def list(self) -> list[data_value_objects.OutputData]:
        #TODO 4: investigate how to connect to postgres database 
        #TODO this is supposed to raise DataAccessException
        logger.info("database list action here")
        return [data_value_objects.OutputData("Bartosz Dżakubczak", 59, False)]
 
