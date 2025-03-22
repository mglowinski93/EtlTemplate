import io
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
from modules.extract.services import commands as service_extract_commands
from modules.load.domain import commands as domain_load_commands
from modules.load.domain.ports import repositories, units_of_work
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
    @inject.param(name="save_file_repository", cls="save_file_repository")
    def create(
        self,
        request: Request,
        data_unit_of_work: units_of_work.AbstractDataUnitOfWork,
        save_file_repository: repositories.AbstractFileSaveRepository
    ) -> Response:
        if "file" not in request.FILES:
            return Response(
                str({common_consts.ERROR_DETAIL_KEY: "File not attached."}),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        try:
            logger.info("Extracting dataset...")
            input_data: data_value_objects.InputData = service_extract_commands.extract(
                    domain_extract_commands.ExtractData(
                        save_file_repository.save(io.BytesIO(request.FILES["file"].read()), request.FILES["file"].name)
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
        except FileNotFoundError as e:
            logger.info(e.args[0])
            return Response(
                str({common_consts.ERROR_DETAIL_KEY: "File not found."}),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except domain_exceptions.FileDataFormatNotSupportedException as e:
            logger.info(str(e.args[0]))
            return Response(
                str({common_consts.ERROR_DETAIL_KEY: "Unsupported file extension."}),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except domain_exceptions.DataValidationException as e:
            logger.info(str(e.args[0]))
            return Response(
                str({common_consts.ERROR_DETAIL_KEY: "Invalid data format."}),
                status=status.HTTP_400_BAD_REQUEST,
            )
        logger.info("Dataset saved.")

        return Response(status=status.HTTP_201_CREATED)
