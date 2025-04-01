import logging

import inject
from drf_spectacular import utils as swagger_utils
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from modules.common import const as common_consts
from modules.extract.domain import commands as domain_commands
from modules.extract.domain import exceptions
from modules.extract.domain import value_objects
from modules.extract.domain.ports import units_of_work
from modules.extract.services import commands
from modules.load.domain import commands as load_domain_commands
from modules.load.domain.ports import units_of_work as load_units_of_work
from modules.load.services import commands as services_load_commands
from modules.transform.domain import commands as domain_transform_commands
from modules.transform.domain import value_objects as transform_value_objects
from modules.transform.services import commands as transform_commands

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
        data_unit_of_work: load_units_of_work.AbstractDataUnitOfWork,
        extract_unit_of_work: units_of_work.AbstractExtractUnitOfWork,
    ) -> Response:
        if "file" not in request.FILES:
            return Response(
                {common_consts.ERROR_DETAIL_KEY: "File not attached."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        logger.info("Extracting dataset...")
        try:
            #todo move it to extract command and use the same context manager to save file and put row to extracthistory
            saved_file_path = extract_unit_of_work.file.save(
                        file=bytes(request.FILES["file"].read()),
                        file_name=request.FILES["file"].name,
                    )
            input_data: value_objects.InputData = commands.extract(
                domain_commands.ExtractData(
                    saved_file_path
                )
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

        logger.info("Saving extract history...")
        commands.save_extract_history(extract_unit_of_work, value_objects.ExtractHistory(
                input_file_name = request.FILES["file"].name, 
                saved_file_name = saved_file_path.name,
        ))
        logger.info("Extract history saved.")

        logger.info("Transforming dataset...")
        output_data: list[
            transform_value_objects.OutputData
        ] = transform_commands.transform(
            domain_transform_commands.TransformData(input_data)
        )
        logger.info("Dataset transformed.")

        logger.info("Saving dataset...")
        services_load_commands.save(
            data_unit_of_work, load_domain_commands.SaveData(output_data)
        )
        logger.info("Dataset saved.")

        return Response(status=status.HTTP_201_CREATED)
