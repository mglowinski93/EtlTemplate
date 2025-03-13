import logging
from pprint import pformat
from typing import Any

from django.contrib.auth import get_user_model

from modules.load.services.queries import ports as query_ports 
from modules.data.domain import value_objects as data_value_objects
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
        result = [map_outputdata_model_to_output_dto(output_data) for output_data in query.all()]

        return result, query.count()


    # def list(
    #     self,
    # ) -> tuple[list[data_value_objects.OutputData], int]:
    #     query = (
    #         Point.objects.prefetch_related("todo", "comments", "author")
    #         .filter(**_get_django_points_filters(filters))
    #         .order_by(*_get_django_points_ordering(ordering))
    #     )
    #     return [
    #         map_point_model_to_output_dto(point)
    #         for point in query.all()[
    #             pagination.offset : pagination.offset + pagination.records_per_page
    #         ]
    #     ], query.count()
