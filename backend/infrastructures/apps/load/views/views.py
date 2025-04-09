import logging

import inject
from drf_spectacular import utils as swagger_utils
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from modules.common import const as common_consts
from modules.common import ordering as common_ordering
from modules.common import pagination as pagination_dtos
from modules.load.domain import value_objects
from modules.load.services.queries import ports as query_ports
from modules.load.services.queries import queries

from ...common import exceptions as common_exceptions
from .serializers import DetailedOutputDataReadSerializer, OutputDataReadSerializer

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
                        "data": {
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
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-04-07T00:00:00Z",
                                },
                            },
                        },
                    },
                },
            ),
            status.HTTP_404_NOT_FOUND: swagger_utils.OpenApiResponse(
                description="Output Data not found.",
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
    def retrieve(
        self,
        request: Request,
        pk: str,
        query_data_repository: query_ports.AbstractDataQueryRepository,
    ):
        try:
            logger.info("Querying Output Data...")
            detailed_output_data = queries.get_data(
                query_data_repository, data_id=value_objects.DataId.from_hex(pk)
            )
        except common_exceptions.DataDoesNotExist:
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Data not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            data={
                "data": DetailedOutputDataReadSerializer(detailed_output_data).data,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_utils.extend_schema(
        responses={
            status.HTTP_200_OK: swagger_utils.OpenApiResponse(
                description="Load all Output Data.",
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
        },
    )
    @inject.param(name="query_data_repository", cls="query_data_repository")
    def list(
        self,
        request: Request,
        query_data_repository: query_ports.AbstractDataQueryRepository,
    ):
        logger.info("Listing all datasets...")
        output_data, count = queries.list_data(
            repository=query_data_repository,
            filters=query_ports.DataFilters(),
            ordering=query_ports.DataOrdering(
                timestamp=common_ordering.Ordering(
                    common_ordering.OrderingOrder.ASCENDING, 0
                )
            ),
            pagination=pagination_dtos.Pagination(
                pagination_dtos.PAGINATION_DEFAULT_OFFSET,
                pagination_dtos.PAGINATION_DEFAULT_LIMIT,
            ),
        )
        logger.info("Listed datasets.")

        return Response(
            data={
                "count": count,
                "data": OutputDataReadSerializer(output_data, many=True).data,
            },
            status=status.HTTP_200_OK,
        )
