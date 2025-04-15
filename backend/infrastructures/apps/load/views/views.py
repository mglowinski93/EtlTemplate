import logging
import uuid

import inject
from drf_spectacular import utils as swagger_utils
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from infrastructures.apps.common import consts as common_consts, pagination as common_pagination
from modules.common import pagination as pagination_dtos
from modules.load.domain import value_objects
from modules.load.services.queries import ports as query_ports
from modules.load.services import queries
from modules.common import ordering as ordering_dtos
from django.core import exceptions as django_exceptions


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
        logger.info("Querying Output Data...")

        try:
            uuid.UUID(pk)
        except ValueError:
            logger.warning("'%s' is invalid format as Data_ID.", pk)
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Data not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            detailed_output_data = queries.get_data(
                query_data_repository, data_id=value_objects.DataId.from_hex(pk)
            )
        except common_exceptions.DataDoesNotExist:
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Data not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        logger.info("Data Queried.")

        return Response(
            data=DetailedOutputDataReadSerializer(detailed_output_data).data,
            status=status.HTTP_200_OK,
        )

    @swagger_utils.extend_schema(
        parameters=[
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name="is_satisfied",
                description="Satisfaction to filter data by.",
                required=False,
                type=bool,
                examples=[
                    swagger_utils.OpenApiExample(name="is_satisfied", value=True),
                ],
            ),
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name="timestamp_from",
                description="Timestamp from date to filter data.",
                required=False,
                type=str,
                examples=[
                    swagger_utils.OpenApiExample("2025-04-08T18:48:38.504419+02:00"),
                ],
            ),
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name="timestamp_to",
                description="Timestamp to date to filter data.",
                required=False,
                type=str,
                examples=[
                    swagger_utils.OpenApiExample("2025-04-08T18:48:38.504419+02:00"),
                ],
            ),            
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name=common_consts.ORDERING_QUERY_PARAMETER_NAME,
                description="Ordering fields separated by commas.\n\n"
                "Prefix '-' before name means descending, without prefix means ascending.",
                required=False,
                type=str,
                examples=[
                    swagger_utils.OpenApiExample("is_satisfied"),
                    swagger_utils.OpenApiExample("-is_satisfied"),
                    swagger_utils.OpenApiExample("timestamp"),
                    swagger_utils.OpenApiExample("-timestamp"),
                ],
            ),
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name=common_consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME,
                description="Number of records to be skipped.",
                required=False,
                type=int,
                default=pagination_dtos.PAGINATION_DEFAULT_OFFSET,
            ),
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name=common_consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME,
                description="Results limit per page.",
                required=False,
                type=int,
                default=pagination_dtos.PAGINATION_DEFAULT_LIMIT,
            ),
        ],    
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
            status.HTTP_400_BAD_REQUEST: swagger_utils.OpenApiResponse(
                description="Invalid query parameters.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "Invalid pagination parameters.",
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
            is_satisfied = _str_to_bool(request.query_params.get("is_satisfied"))
        except (ValueError, TypeError):
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Invalid filtering parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )   
        filters=query_ports.DataFilters(
            is_satisfied=is_satisfied,
            timestamp_from=request.query_params.get("timestamp_from"),
            timestamp_to=request.query_params.get("timestamp_to"),
        ) 
        logger.info("Filters: %s", filters)

        _ordering = ordering_dtos.Ordering.create_ordering(
            request.query_params[common_consts.ORDERING_QUERY_PARAMETER_NAME].split(",")
            if common_consts.ORDERING_QUERY_PARAMETER_NAME in request.query_params
            else {}
        )
        ordering = query_ports.DataOrdering(
            timestamp=_ordering.get("timestamp"),
        )        
        logger.info("Ordering: %s", ordering)


        try:
            pagination = pagination_dtos.Pagination(
                offset=request.query_params.get(
                    common_consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME,
                    pagination_dtos.PAGINATION_DEFAULT_OFFSET,
                ),
                records_per_page=request.query_params.get(
                    common_consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME,
                    pagination_dtos.PAGINATION_DEFAULT_LIMIT,
                ),
            )
        except ValueError:
            logger.warning("Invalid pagination parameters.")
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Invalid pagination parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logger.info("Pagination: %s", pagination)

        try:
            results: list[queries.OutputData]
            count: int 
            results, count = queries.list_data(
                repository=query_data_repository,
                filters=filters,
                ordering=ordering,
                pagination=pagination,
            )
        except django_exceptions.ValidationError:
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Invalid query parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logger.info("Dataset listed successfully.")

        return Response(
            data=common_pagination.make_paginated_response(
                url=request.build_absolute_uri(),
                count=count,
                offset=pagination.offset,
                records_per_page=pagination.records_per_page,
                results=[OutputDataReadSerializer(output_data).data for output_data in results],
            ).data, 
            status=status.HTTP_200_OK,
        )
    
def _str_to_bool(value: str) -> bool | None:
    if value is None:
        return None
    val = value.strip().lower()
    if val == "true":
        return True
    elif val == "false":
        return False
    else:
        raise ValueError()
