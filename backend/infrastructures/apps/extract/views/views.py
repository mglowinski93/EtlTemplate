import logging

import inject
from drf_spectacular import utils as swagger_utils
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from infrastructures.apps.common import consts as common_consts
from modules.extract.domain import commands as domain_commands
from modules.extract.domain import exceptions, ports, value_objects
from modules.extract.services import commands
from modules.load.domain import commands as load_domain_commands
from modules.load.domain import ports as load_ports
from modules.load.services import commands as load_commands
from modules.transform.domain import commands as transform_domain_commands
from modules.transform.domain import value_objects as transform_value_objects
from modules.transform.services import commands as transform_commands

from ...common import exceptions as common_exceptions
from ..exceptions import FileSaveError

logger = logging.getLogger(__name__)


class ExtractViewSet(
    ViewSet,
):
    @swagger_utils.extend_schema(
        responses={
            status.HTTP_201_CREATED: swagger_utils.OpenApiResponse(
                description="Transformed and saved data successfully.",
            ),
            status.HTTP_400_BAD_REQUEST: swagger_utils.OpenApiResponse(
                description="Issue occurred while processing dataset.",
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
    @inject.param(name="data_unit_of_work", cls="data_unit_of_work")
    @inject.param(name="extract_unit_of_work", cls="extract_unit_of_work")
    def create(
        self,
        request: Request,
        data_unit_of_work: load_ports.AbstractDataUnitOfWork,
        extract_unit_of_work: ports.AbstractExtractUnitOfWork,
    ) -> Response:
        if "file" not in request.FILES:
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "File not attached."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        logger.info("Extracting dataset...")
        try:
            input_data: value_objects.InputData = commands.extract(
                extract_unit_of_work=extract_unit_of_work,
                command=domain_commands.ExtractData(
                    file=bytes(request.FILES["file"].read()),
                    file_name=request.FILES["file"].name,
                ),
            )
        except FileSaveError as err:
            logger.error("Can not save file '%s'.", err.file_name)
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Can not save file."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except exceptions.FileExtensionNotSupportedError as err:
            logger.error(
                "Can not extract data from file '%s', due to not supported extension.",
                err.file_extension,
            )
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Unsupported file extension."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except exceptions.DataValidationError as err:
            logger.error("Invalid input data in file '%s'.", err.file_name)
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Invalid data format."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logger.info("Dataset extracted.")

        logger.info("Transforming dataset...")
        transformed_data: list[
            transform_value_objects.TransformedData
        ] = transform_commands.transform(
            transform_domain_commands.TransformData(input_data)
        )
        logger.info("Dataset transformed.")

        logger.info("Saving dataset...")
        try:
            load_commands.save(
                unit_of_work=data_unit_of_work,
                command=load_domain_commands.SaveData(transformed_data),
            )
        except common_exceptions.DatabaseError:
            logger.error("Database connection issue, can not save output data.")
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        logger.info("Dataset saved.")

        return Response(status=status.HTTP_201_CREATED)
