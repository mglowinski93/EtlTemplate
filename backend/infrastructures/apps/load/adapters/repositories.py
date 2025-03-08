import logging
from pprint import pformat
from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from modules.load.domain.ports import repositories as domain_repositories 
from modules.data.domain import value_objects as data_value_objects



logger = logging.getLogger(__name__)
User = get_user_model()


class DjangoDataDomainRepository(domain_repositories.AbstractDataDomainRepository):
    """
    See description of parent class to get more details.
    """
    def create(self, data: list[data_value_objects.OutputData]) -> None:
        #TODO this is supposed to raise DataCreationException
        logger.info("database load action here")
 





