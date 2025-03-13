import logging
from pprint import pformat
from typing import Any

from django.contrib.auth import get_user_model

from modules.data.domain import value_objects as data_value_objects
from modules.load.domain.ports import repositories as domain_repositories

from ..models import OutputData

logger = logging.getLogger(__name__)


class DjangoDataDomainRepository(domain_repositories.AbstractDataDomainRepository):
    """
    See description of parent class to get more details.
    """

    def create(self, data: list[data_value_objects.OutputData]) -> None:
        OutputData.objects.bulk_create(
            [
                OutputData(
                    full_name=output_data.full_name,
                    age=output_data.age,
                    is_satisfied=output_data.is_satisfied,
                )
                for output_data in data
            ]
        )
