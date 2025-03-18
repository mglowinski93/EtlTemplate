import logging

import inject
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from modules.common import pagination as pagination_dtos

from modules.load.services.queries import ports as query_ports

from .serializers import OutputDataReadSerializer

logger = logging.getLogger(__name__)


class LoadViewSet(
    ViewSet,
):
    @inject.param(name="query_data_repository", cls="query_data_repository")
    def list(
        self,
        request: Request,
        query_data_repository: query_ports.AbstractDataQueryRepository,
    ):
        logger.info("Listing all datasets...")
        #TODO: fix load view set by defining filter, pagination and ordering and add them here
        output_data, count = query_data_repository.list(
            filters = query_ports.OutputDataFilters(),
        ordering = query_ports.OutputDataOrdering(),
        pagination = pagination_dtos.Pagination(pagination_dtos.PAGINATION_DEFAULT_OFFSET, pagination_dtos.PAGINATION_DEFAULT_LIMIT)
        )
        return Response(
            data={
                "count": count,
                "data": OutputDataReadSerializer(output_data, many=True).data,
            },
            status=status.HTTP_200_OK,
        )
