import logging

from modules.load.services import queries as load_queries
from modules.load.domain.ports import repositories as domain_repositories

from infrastructures.apps.load.models import Data


logger = logging.getLogger(__name__)

class DjangoDataDomainRepository(domain_repositories.AbstractDataDomainRepository):
    """
    See description of parent class to get more details.
    """

    def create(self, data: list[load_queries.OutputData]) -> None:
        Data.objects.bulk_create(
            [
                Data(
                    data={
                        "full_name": output_data.full_name,
                        "age": output_data.age,
                        "is_satisfied": output_data.is_satisfied,
                    }
                )
                for output_data in data
            ]
        )
