import logging

from modules.data.domain import value_objects as data_value_objects
from modules.load.domain.ports import repositories as domain_repositories
from modules.load.services.queries import ports as query_ports

from ..models import OutputData
from .mappers import map_outputdata_model_to_output_dto

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

class DjangoDataQueryRepository(query_ports.AbstractDataQueryRepository):
    """
    See description of parent class to get more details.
    """

    def list(self) -> tuple[list[data_value_objects.OutputData], int]:
        query = OutputData.objects
        result = [
            map_outputdata_model_to_output_dto(output_data)
            for output_data in query.all()
        ]

        return result, query.count()
