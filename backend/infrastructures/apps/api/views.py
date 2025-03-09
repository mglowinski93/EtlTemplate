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
from modules.data.domain import value_objects as domain_value_objects
from serializers import ExtractDataSerializer, InputDataSerializer, OutputDataListSerializer
import pandera as pa

from modules.common.domain.ports import units_of_work

from modules.common.domain.exceptions import DataValidationException


logger = logging.getLogger(__name__)

    #TODO 2: Should we break views.py into 3 separate files, each file under corresponding django application? Or can we keep whole api together in one file? 
class DataViewSet(
    ViewSet,
):
    def extract(
        self,
        request: Request,
    ) -> Response:
        logger.info("Extracting Dataset...")

        serializer = ExtractDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            extract_command = domain_extract_commands.ExtractData(serializer.validated_data["file_path"])
            return Response(
                data=InputDataSerializer(service_extract_commands.extract(extract_command)).data,
                status=status.HTTP_200_OK,
            )
        except DataValidationException as err:
           return Response({"error": "invalid input"}, status=status.HTTP_400_BAD_REQUEST)
    

    def transform(
        self,
        request: Request,
    ) -> Response:
        logger.info("Transforming Dataset...")
        serializer = InputDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        transform_command = domain_transform_commands.TransformData(serializer.create(serializer.validated_data))
        return Response(
            data= OutputDataListSerializer(services_transform_commands.transform(transform_command)).data,
            status=status.HTTP_200_OK
        )

    #TODO 1: how to inject save_data_repository into unit of work ?
    @inject.param(name="save_data_unit_of_work", cls="save_data_unit_of_work")
    @inject.param(name="save_data_repository", cls="save_data_repository")
    def save(
        self,
        request: Request, 
        save_data_unit_of_work: units_of_work.AbstractUnitOfWork,
    ) -> Response:
        logger.info("Saving Dataset...")
        serializer = OutputDataListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        
        save_command = domain_load_commands.SaveData(serializer.create(serializer.validated_data))
        services_load_commands.save(save_command, save_data_unit_of_work)
        return Response(
            status=status.HTTP_201_CREATED
        )
