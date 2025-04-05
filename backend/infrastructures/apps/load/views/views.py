import logging

import inject
from drf_spectacular import utils as swagger_utils
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from modules.common import ordering as common_ordering
from modules.common import pagination as pagination_dtos
from modules.load.services.queries import ports as query_ports

from .serializers import OutputDataReadSerializer
from ...common import exceptions as common_exceptions
from modules.common import const as common_consts

logger = logging.getLogger(__name__)


class LoadViewSet(
    ViewSet,
):
    @swagger_utils.extend_schema(
        responses={
            status.HTTP_200_OK: swagger_utils.OpenApiResponse(
                description="Issue occurred while processing dataset.",
                response={
                    "type": "object",
                    "properties": {
                        "count": {
                            "type": "integer",
                            "example": 10,
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "full_name": {
                                        "type": "string",
                                        "example": "John Snow",
                                    },
                                    "age": {"type": "integer", "example": 20},
                                    "is_satisfied": {
                                        "type": "boolean",
                                        "example": True,
                                    },
                                },
                            },
                        },
                    },
                },
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: swagger_utils.OpenApiResponse(
                description="Internal application issue.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "",
                        }
                    },
                },
            ),
        },
    )
    @inject.param(name="query_data_repository", cls="query_data_repository")
    def list(
        self,
        request: Request,
        query_data_repository: query_ports.AbstractDataQueryRepository,
    ):
        logger.info("Listing all datasets...")
        try: 
            output_data, count = query_data_repository.list(
                ordering=query_ports.DataOrdering(
                    timestamp=common_ordering.Ordering(
                        common_ordering.OrderingOrder.ASCENDING, 0
                    )
                ),
                filters=query_ports.DataFilters(),
                pagination=pagination_dtos.Pagination(
                    pagination_dtos.PAGINATION_DEFAULT_OFFSET,
                    pagination_dtos.PAGINATION_DEFAULT_LIMIT,
                ),
            )
        except common_exceptions.DatabaseError as err:
            logger.error(
                "Database connection issue, can not query output data."
            )
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        logger.info("Listed datasets.")

        return Response(
            data={
                "count": count,
                "data": OutputDataReadSerializer(output_data, many=True).data,
            },
            status=status.HTTP_200_OK,
        )
