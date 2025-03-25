import logging

import inject
from drf_spectacular import utils as swagger_utils
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from modules.common import const as common_consts
from modules.common.domain import exceptions as domain_exceptions
from modules.data.domain import value_objects as data_value_objects
from modules.extract.domain import commands as domain_extract_commands
from modules.extract.domain.ports import units_of_work as extract_units_of_work
from modules.extract.services import commands as service_extract_commands
from modules.load.domain import commands as domain_load_commands
from modules.load.domain.ports import units_of_work as load_units_of_work
from modules.load.services import commands as services_load_commands
from modules.load.services import queries as load_queries
from modules.transform.domain import commands as domain_transform_commands
from modules.transform.services import commands as services_transform_commands

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
        },
    )
    @inject.param(name="data_unit_of_work", cls="data_unit_of_work")
    @inject.param(name="file_unit_of_work", cls="file_unit_of_work")
    def create(
        self,
        request: Request,
        data_unit_of_work: load_units_of_work.AbstractDataUnitOfWork,
        file_unit_of_work: extract_units_of_work.AbstractFileUnitOfWork,
    ) -> Response:
        if "file" not in request.FILES:
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "File not attached."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        try:
            logger.info("Extracting dataset...")
            input_data: data_value_objects.InputData = service_extract_commands.extract(
                domain_extract_commands.ExtractData(
                    file_unit_of_work.file.save(
                        bytes(request.FILES["file"].read()), request.FILES["file"].name
                    )
                )
            )
            logger.info("Dataset extracted.")

            logger.info("Transforming dataset...")
            output_data: list[
                load_queries.OutputData
            ] = services_transform_commands.transform(
                domain_transform_commands.TransformData(input_data)
            )
            logger.info("Dataset transformed.")

            logger.info("Saving dataset...")
            services_load_commands.save(
                data_unit_of_work, domain_load_commands.SaveData(output_data)
            )
        except domain_exceptions.FileNotFoundError as err:
            logger.error("File to extract data from not found. File name: %s", err.file_name)
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "File not found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except domain_exceptions.FileExtensionNotSupportedError as err:
            logger.error("Can not extract data from file %s, due to not supported extension", err.file_extension)
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Unsupported file extension."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except domain_exceptions.DataValidationError as err:
            logger.error("Invalid input data in file %s", err.file_name)
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "Invalid data format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)
