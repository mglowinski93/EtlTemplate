import logging
from datetime import datetime

import inject
from drf_spectacular import utils as swagger_utils
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from modules.transform.domain import commands as domain_transform_commands
from modules.transform.services import commands as services_transform_commands
from modules.extract.domain import commands as domain_extract_commands
from modules.extract.services import commands as service_extract_commands
from modules.load.domain import commands as domain_load_commands
from modules.load.services import commands as services_load_commands
from modules.load.services.queries import ports as query_ports
from modules.data.domain import value_objects as data_value_objects
from .serializers import ExtractDataSerializer, OutputDataSerializer
import pandera as pa
from typing import List
from pathlib import Path


from modules.common.domain.ports import units_of_work

from modules.common.domain import exceptions as domain_exceptions

import pandas as pd


logger = logging.getLogger(__name__)


class DataViewSet(
    ViewSet,
):

    @inject.param(name="save_data_unit_of_work", cls="save_data_unit_of_work")
    def create(
        self,
        request: Request, 
        save_data_unit_of_work: units_of_work.AbstractUnitOfWork,
    ) -> Response:
        logger.info("Extracting Dataset...")

        serializer = ExtractDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        try:
            
            input_data: data_value_objects.InputData[pd.DataFrame] = service_extract_commands.extract(domain_extract_commands.ExtractData(Path(serializer.validated_data["file_path"])))
            logger.info("Transforming Dataset...")
            output_data : list[data_value_objects.OutputData] = services_transform_commands.transform(domain_transform_commands.TransformData(input_data))
            logger.info("Saving Dataset...")
            services_load_commands.save(save_data_unit_of_work, domain_load_commands.SaveData(output_data))
        except FileNotFoundError as err:
            return Response({"error": "file not found", "file_path": serializer.validated_data["file_path"]}, status=status.HTTP_400_BAD_REQUEST)
        except domain_exceptions.DataValidationException as err:
            return Response({"error": "invalid input data", "file_path": serializer.validated_data["file_path"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            status=status.HTTP_200_OK
        )

    @inject.param(name="query_data_repository", cls="query_data_repository")
    def list(self, request: Request, query_data_repository: query_ports.AbstractDataQueryRepository):
        logger.info("Listing all datasets...")
        output_data, count = query_data_repository.list()
        return Response(
            data={"count": count, "data": OutputDataSerializer(output_data, many=True).data},
            status=status.HTTP_200_OK,
        )



