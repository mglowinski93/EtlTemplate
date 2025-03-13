import logging

from modules.data.domain import value_objects as data_value_objects
from modules.load.services.queries import ports as query_ports

from ...load.models import OutputData
from .mappers import map_outputdata_model_to_output_dto

logger = logging.getLogger(__name__)


class DjangoDataQueryRepository(query_ports.AbstractDataQueryRepository):
    """
    See description of parent class to get more details.
    """

    def list(self) -> tuple[list[data_value_objects.OutputData], int]:
        logger.info("database list action here")
        query = OutputData.objects
        result = [
            map_outputdata_model_to_output_dto(output_data)
            for output_data in query.all()
        ]

        return result, query.count()
