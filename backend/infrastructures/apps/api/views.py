import logging
from datetime import datetime

import inject
from drf_spectacular import utils as swagger_utils
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


from modules.extract.domain import commands as domain_extract_commands
from modules.extract.services import commands as service_extract_commands
from serializers import ExtractDataSerializer, InputDataSerializer
import pandera as pa

from modules.common.domain.exceptions import DataValidationException


logger = logging.getLogger(__name__)


class DataViewSet(
    ViewSet,
):


    @inject.param(name="todos_query_repository", cls="todos_query_repository")
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


            































    @swagger_utils.extend_schema(
        parameters=[
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name="author_id",
                description="Author ID to filter todos by.",
                required=False,
                type=int,
                examples=[
                    swagger_utils.OpenApiExample("1"),
                ],
            ),
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name="title",
                description="Title of todo to filter todos by.",
                required=False,
                type=str,
                examples=[
                    swagger_utils.OpenApiExample("Legs training"),
                ],
            ),
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name="type",
                description="Type of todo to filter todos by.",
                required=False,
                type=str,
                enum=value_objects.TodoType.list(),
                examples=[
                    swagger_utils.OpenApiExample(todo_type)
                    for todo_type in value_objects.TodoType.list()
                ],
            ),
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name="execute_at_from",
                description="Date and time of todo execution to filter todos from.",
                required=False,
                type=datetime,
                examples=[
                    swagger_utils.OpenApiExample("2024-04-10T01:20:51+00:00"),
                ],
            ),
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.QUERY,
                name="execute_at_to",
                description="Date and time of todo execution to filter todos to.",
                required=False,
                type=datetime,
                examples=[
                    swagger_utils.OpenApiExample("2024-04-10T01:20:51+00:00"),
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
                    swagger_utils.OpenApiExample("title"),
                    swagger_utils.OpenApiExample("-title"),
                    swagger_utils.OpenApiExample("type"),
                    swagger_utils.OpenApiExample("-type"),
                    swagger_utils.OpenApiExample("execute_at"),
                    swagger_utils.OpenApiExample("-execute_at"),
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
                description="Retrieved todos successfully.",
                response=common_swagger.enveloper(TodoReadSerializer, many=True),
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
            status.HTTP_401_UNAUTHORIZED: swagger_utils.OpenApiResponse(
                description="User not authenticated.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "Authentication credentials were not provided.",
                        }
                    },
                },
            ),
        },
    )
    @inject.param(name="todos_query_repository", cls="todos_query_repository")
    def list(
        self,
        request: Request,
        todos_query_repository: query_ports.AbstractTodosQueryRepository,
    ) -> Response:
        logger.info("Listing todos...")

        author_id = None
        author_id_key = "author_id"
        if author_id_key in request.query_params:
            try:
                author_id = int(request.query_params[author_id_key])
            except ValueError as err:
                logger.warning(
                    "'%s' is invalid format as %s.",
                    request.query_params[author_id_key],
                    author_id_key,
                )
                raise exceptions.ValidationError(
                    {
                        common_consts.ERROR_DETAIL_KEY: f"Badly formed integer as {author_id_key}."
                    }
                ) from err

            if author_id < 0:
                logger.warning(
                    "%s can't be negative number: '%s'.",
                    author_id_key,
                    request.query_params[author_id_key],
                )
                raise exceptions.ValidationError(
                    {
                        common_consts.ERROR_DETAIL_KEY: f"{author_id_key} must be a positive integer."
                    }
                )

        type_ = None
        type_key = "type"
        if type_key in request.query_params:
            try:
                type_ = value_objects.TodoType(request.query_params[type_key])
            except ValueError as err:
                logger.warning(
                    "'%s' is invalid format as todo %s.",
                    request.query_params[type_key],
                    type_key,
                )
                raise exceptions.ValidationError(
                    {common_consts.ERROR_DETAIL_KEY: "Invalid todo type."}
                ) from err

        execute_at_from = None
        execute_at_from_key = "execute_at_from"
        if execute_at_from_key in request.query_params:
            try:
                execute_at_from = datetime.fromisoformat(
                    request.query_params[execute_at_from_key]
                )
            except ValueError as err:
                logger.warning(
                    "'%s' is invalid format as %s key.",
                    request.query_params[execute_at_from_key],
                    execute_at_from_key,
                )
                raise exceptions.ValidationError(
                    {
                        common_consts.ERROR_DETAIL_KEY: f"Badly formed datetime string as {execute_at_from_key}."
                    }
                ) from err

        execute_at_to = None
        execute_at_to_key = "execute_at_to"
        if execute_at_to_key in request.query_params:
            try:
                execute_at_to = datetime.fromisoformat(
                    request.query_params[execute_at_to_key]
                )
            except ValueError as err:
                logger.warning(
                    "'%s' is invalid format as %s key.",
                    request.query_params[execute_at_to_key],
                    execute_at_to_key,
                )
                raise exceptions.ValidationError(
                    {
                        common_consts.ERROR_DETAIL_KEY: f"Badly formed datetime string as {execute_at_to_key}."
                    }
                ) from err

        filters = query_ports.TodoFilters(
            author_id=author_id,
            executor_id=request.user.id,
            title=request.query_params.get("title"),
            type=type_,
            execute_at_from=execute_at_from,
            execute_at_to=execute_at_to,
        )
        logger.info("Filters: %s", filters)

        _ordering = ordering_dtos.Ordering.create_ordering(
            request.query_params[common_consts.ORDERING_QUERY_PARAMETER_NAME].split(",")
            if common_consts.ORDERING_QUERY_PARAMETER_NAME in request.query_params
            else {}
        )
        ordering = query_ports.TodoOrdering(
            title=_ordering.get("title"),
            type=_ordering.get("type"),
            execute_at=_ordering.get("execute_at"),
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
        except ValueError as err:
            logger.warning("Invalid pagination parameters.")
            raise exceptions.ValidationError(
                {common_consts.ERROR_DETAIL_KEY: "Invalid pagination parameters."}
            ) from err
        logger.info("Pagination: %s", pagination)

        results: list[queries.OutputTodo]
        count: int
        results, count = queries.list_todos(
            repository=todos_query_repository,
            filters=filters,
            ordering=ordering,
            pagination=pagination,
        )

        logger.info("Todos listed successfully.")
        return Response(
            data=common_pagination.make_paginated_response(
                url=request.build_absolute_uri(),
                count=count,
                offset=pagination.offset,
                records_per_page=pagination.records_per_page,
                results=[self.serializer_class(todo).data for todo in results],
            ).data,
            status=status.HTTP_200_OK,
        )

    @swagger_utils.extend_schema(
        request=TodoCreateSerializer,
        responses={
            status.HTTP_201_CREATED: swagger_utils.OpenApiResponse(
                description="Created todo successfully.",
                response=TodoCreatedSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: swagger_utils.OpenApiResponse(
                description="Issue occurred while creating todo.",
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
            status.HTTP_401_UNAUTHORIZED: swagger_utils.OpenApiResponse(
                description="User not authenticated.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "Authentication credentials were not provided.",
                        }
                    },
                },
            ),
        },
    )
    @inject.param(name="todos_unit_of_work", cls="todos_unit_of_work")
    @inject.param(name="message_bus", cls="message_bus")
    def create(
        self,
        request: Request,
        todos_unit_of_work: domain_ports.AbstractTodosUnitOfWork,
        message_bus: common_message_bus.MessageBus,
    ) -> Response:
        serializer = TodoCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            todo: entities.Todo = commands.create_todo(
                todos_unit_of_work=todos_unit_of_work,
                message_bus=message_bus,
                command=domain_commands.CreateTodo(
                    requester_id=request.user.id,
                    executor_id=request.user.id,
                    title=serializer.validated_data["title"],
                    description=serializer.validated_data["description"],
                    type=value_objects.TodoType(serializer.validated_data["type"]),
                    execute_at=serializer.validated_data["execute_at"],
                ),
            )
        except domain_exceptions.AuthorDoesNotExist:
            logger.warning("Author with ID '%s' does not exist.", request.user.id)
            raise exceptions.ValidationError({common_consts.ERROR_DETAIL_KEY: ""})
        except domain_exceptions.ExecutorDoesNotExist:
            logger.warning(
                "Executor with ID '%s' does not exist.",
                serializer.validated_data["executor_id"],
            )
            raise exceptions.ValidationError({common_consts.ERROR_DETAIL_KEY: ""})

        return Response(
            data=TodoCreatedSerializer(todo).data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_utils.extend_schema(
        parameters=[
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.PATH,
                name="id",
                description="ID of todo to update.",
                required=True,
                type=str,
            )
        ],
        responses={
            status.HTTP_200_OK: swagger_utils.OpenApiResponse(
                description="Updated todo successfully.",
                response=TodoUpdatedSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: swagger_utils.OpenApiResponse(
                description="Issue occurred while updating todo.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "User can't update todo with ID, since it is not his own.",
                        }
                    },
                },
            ),
            status.HTTP_401_UNAUTHORIZED: swagger_utils.OpenApiResponse(
                description="User not authenticated.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "Authentication credentials were not provided.",
                        }
                    },
                },
            ),
            status.HTTP_404_NOT_FOUND: swagger_utils.OpenApiResponse(
                description="Todo with specified ID does not exist.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "Not found.",
                        }
                    },
                },
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: swagger_utils.OpenApiResponse(
                description="Invalid input data.",
                response={
                    "type": "object",
                    "properties": {
                        "field_name": {
                            "type": "object",
                            "properties": {"field_name": {"type": "array"}},
                        }
                    },
                },
            ),
        },
    )
    @inject.param(name="todos_unit_of_work", cls="todos_unit_of_work")
    @inject.param(name="message_bus", cls="message_bus")
    def update(
        self,
        request,
        pk,
        todos_unit_of_work: domain_ports.AbstractTodosUnitOfWork,
        message_bus: common_message_bus.MessageBus,
    ) -> Response:
        try:
            todo_id = value_objects.TodoId(pk)
        except ValueError as err:
            logger.warning("'%s' is invalid format as todo ID.", pk)
            raise exceptions.NotFound(
                {common_consts.ERROR_DETAIL_KEY: "Not found."}
            ) from err

        serializer = TodoUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            todo: entities.Todo = commands.update_todo(
                todos_unit_of_work=todos_unit_of_work,
                message_bus=message_bus,
                command=domain_commands.UpdateTodo(
                    todo_id=todo_id,
                    requester_id=request.user.id,
                    executor_id=request.user.id,
                    title=serializer.validated_data["title"],
                    description=serializer.validated_data["description"],
                    type=value_objects.TodoType(serializer.validated_data["type"]),
                    execute_at=serializer.validated_data["execute_at"],
                ),
            )
        except domain_exceptions.UserCanNotUpdateOtherAuthorTodo:
            logger.warning(
                "User can't update todo with ID '%s', since it is not his own.",
                pk,
            )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
        except domain_exceptions.TodoDoesNotExist:
            logger.warning("Todo with ID '%s' does not exist.", pk)
            raise exceptions.NotFound({common_consts.ERROR_DETAIL_KEY: "Not found."})
        except domain_exceptions.AuthorDoesNotExist:
            logger.warning("Author with ID '%s' does not exist.", request.user.id)
            raise exceptions.ValidationError({common_consts.ERROR_DETAIL_KEY: ""})
        except domain_exceptions.ExecutorDoesNotExist:
            logger.warning(
                "Executor with ID '%s' does not exist.",
                serializer.validated_data["executor_id"],
            )
            raise exceptions.ValidationError({common_consts.ERROR_DETAIL_KEY: ""})

        return Response(
            data=TodoUpdatedSerializer(todo).data,
            status=status.HTTP_200_OK,
        )

    @swagger_utils.extend_schema(
        parameters=[
            swagger_utils.OpenApiParameter(
                location=swagger_utils.OpenApiParameter.PATH,
                name="id",
                description="ID of todo to delete.",
                required=True,
                type=str,
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: swagger_utils.OpenApiResponse(
                description="Deleted todo successfully.",
            ),
            status.HTTP_400_BAD_REQUEST: swagger_utils.OpenApiResponse(
                description="Issue occurred while deleting todo.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "User can't delete todo with ID, since it is not his own.",
                        }
                    },
                },
            ),
            status.HTTP_401_UNAUTHORIZED: swagger_utils.OpenApiResponse(
                description="User not authenticated.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "Authentication credentials were not provided.",
                        }
                    },
                },
            ),
            status.HTTP_404_NOT_FOUND: swagger_utils.OpenApiResponse(
                description="Todo with specified ID does not exist.",
                response={
                    "type": "object",
                    "properties": {
                        common_consts.ERROR_DETAIL_KEY: {
                            "type": "string",
                            "example": "Not found.",
                        }
                    },
                },
            ),
        },
    )
    @inject.param(name="todos_unit_of_work", cls="todos_unit_of_work")
    @inject.param(name="message_bus", cls="message_bus")
    def delete(
        self,
        request,
        pk,
        todos_unit_of_work: domain_ports.AbstractTodosUnitOfWork,
        message_bus: common_message_bus.MessageBus,
    ) -> Response:
        try:
            todo_id = value_objects.TodoId(pk)
        except ValueError as err:
            logger.warning("'%s' is invalid format as todo ID.", pk)
            raise exceptions.NotFound(
                {common_consts.ERROR_DETAIL_KEY: "Not found."}
            ) from err

        try:
            commands.delete_todo(
                todos_unit_of_work=todos_unit_of_work,
                message_bus=message_bus,
                command=domain_commands.DeleteTodo(
                    todo_id=todo_id, requester_id=request.user.id
                ),
            )
        except domain_exceptions.UserCanNotDeleteOtherAuthorTodo:
            logger.warning(
                "User can't delete todo with ID '%s', since it is not his own.",
                pk,
            )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
        except domain_exceptions.TodoDoesNotExist:
            logger.warning("Todo with ID '%s' does not exist.", pk)
            raise exceptions.NotFound({common_consts.ERROR_DETAIL_KEY: "Not found."})

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
