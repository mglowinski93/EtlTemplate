import logging
from pprint import pformat
from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from modules.common import ordering as ordering_dtos, pagination as pagination_dtos
from modules.todos.domain import (
    entities,
    value_objects,
    exceptions as domain_exceptions,
    ports as domain_ports,
)
from modules.todos.services.queries import dtos as query_dtos, ports as query_ports
from modules.users.domain import (
    value_objects as user_value_objects,
)
from .mappers import (
    map_comment_model_to_output_dto,
    map_point_model_to_output_dto,
    map_todo_model_to_output_dto,
)
from ..models import Comment, Point, Todo
from ...common import ordering as common_ordering


logger = logging.getLogger(_name_)
User = get_user_model()


class DjangoTodosDomainRepository(domain_ports.AbstractTodosDomainRepository):
    """
    See description of parent class to get more details.
    """

    def get(
        self,
        todo_id: value_objects.TodoId,
        executor_id: user_value_objects.USER_ID_TYPE | None = None,
    ) -> entities.Todo:
        query_data = {"id": todo_id}
        if executor_id is not None:
            query_data["executor_id"] = executor_id  # type: ignore[assignment]

        try:
            return (
                Todo.objects.prefetch_related("points", "author", "executor")
                .select_for_update()
                .get(**query_data)
                .to_entity()
            )
        except Todo.DoesNotExist as err:
            logger.warning(
                "Failed to retrieve todo, due to missing todo with ID '%s'.",
                todo_id,
            )
            raise domain_exceptions.TodoDoesNotExist(
                f"Todo with ID '{todo_id}' doesn't exist."
            ) from err

    def create(self, todo: entities.Todo) -> None:
        executor_id = todo.executor_id

        try:
            author = User.objects.get(id=todo.author_id)
        except User.DoesNotExist as err:
            logger.warning(
                "Failed to create todo, due to missing author with ID '%s'.",
                todo.author_id,
            )
            raise domain_exceptions.AuthorDoesNotExist(
                f"Author with ID '{todo.author_id}' doesn't exist."
            ) from err

        try:
            executor = User.objects.get(id=executor_id)
        except User.DoesNotExist as err:
            logger.warning(
                "Failed to create todo, due to missing executor with ID '%s'.",
                executor_id,
            )
            raise domain_exceptions.ExecutorDoesNotExist(
                f"Executor with ID '{executor_id}' doesn't exist."
            ) from err

        Todo.objects.create(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            type=todo.type.name,
            execute_at=todo.execute_at,
            author=author,
            executor=executor,
            created_at=todo.timestamp,
        )

    def update(self, todo: entities.Todo) -> None:
        todo_id = todo.id
        executor_id = todo.executor_id

        try:
            todo_ = Todo.objects.select_for_update().get(id=todo_id)
        except Todo.DoesNotExist as err:
            logger.warning(
                "Failed to update todo, due to missing todo with ID '%s'.",
                todo_id,
            )
            raise domain_exceptions.TodoDoesNotExist(
                f"Todo with ID '{todo_id}' doesn't exist."
            ) from err

        todo_.title = todo.title
        todo_.description = todo.description
        todo_.type = todo.type.name
        todo_.execute_at = todo.execute_at
        try:
            todo_.executor_id = User.objects.get(id=executor_id).id
        except User.DoesNotExist as err:
            logger.warning(
                "Failed to update todo, due to missing executor with ID '%s'.",
                executor_id,
            )
            raise domain_exceptions.ExecutorDoesNotExist(
                f"Executor with ID '{executor_id}' doesn't exist."
            ) from err

        todo_.save()

    def delete(self, todo_id: value_objects.TodoId) -> None:
        try:
            Todo.objects.get(id=todo_id).delete()
        except Todo.DoesNotExist as err:
            logger.warning(
                "Failed to delete todo, due to missing todo with ID '%s'.",
                todo_id,
            )
            raise domain_exceptions.TodoDoesNotExist(
                f"Todo with ID '{todo_id}' doesn't exist."
            ) from err

    @transaction.atomic
    def create_set(self, todos: list[entities.Todo]) -> None:

        author_ids_to_check = (
            {todo.author_id for todo in todos}
            | {point.author_id for todo in todos for point in todo.points}
            | {
                comment.author_id
                for todo in todos
                for point in todo.points
                for comment in point.comments
            }
        )
        missing_author_ids = author_ids_to_check - set(
            User.objects.filter(id__in=author_ids_to_check).values_list("id", flat=True)
        )
        if missing_author_ids:
            logger.warning(
                "Failed to create todos set, due to missing authors with IDs:\n%s",
                pformat(missing_author_ids),
            )
            raise domain_exceptions.AuthorDoesNotExist(
                f"Authors with IDs doesn't exist: \n{pformat(missing_author_ids)}"
            )
        executor_ids_to_check = {todo.executor_id for todo in todos}
        missing_executor_ids = executor_ids_to_check - set(
            User.objects.filter(id__in=executor_ids_to_check).values_list(
                "id", flat=True
            )
        )
        if missing_executor_ids:
            logger.warning(
                "Failed to create todos set, due to missing executors with IDs:\n%s",
                pformat(missing_executor_ids),
            )
            raise domain_exceptions.ExecutorDoesNotExist(
                f"Executors with IDs doesn't exist: \n{pformat(missing_executor_ids)}"
            )
        Todo.objects.bulk_create(
            [
                Todo(
                    id=todo.id,
                    title=todo.title,
                    description=todo.description,
                    type=todo.type.name,
                    execute_at=todo.execute_at,
                    author_id=todo.author_id,
                    executor_id=todo.executor_id,
                    created_at=todo.timestamp,
                )
                for todo in todos
            ]
        )

        todo_ids_to_check = {point.todo_id for todo in todos for point in todo.points}
        missing_todo_ids = todo_ids_to_check - {
            value_objects.TodoId(todo_id.hex)
            for todo_id in Todo.objects.filter(id__in=todo_ids_to_check).values_list(
                "id", flat=True
            )
        }
        if missing_todo_ids:
            logger.warning(
                "Failed to create todos set, due to missing todos with IDs:\n%s",
                pformat(missing_todo_ids),
            )
            raise domain_exceptions.TodoDoesNotExist(
                f"Todos with IDs doesn't exist: \n{pformat(missing_todo_ids)}"
            )
        Point.objects.bulk_create(
            [
                Point(
                    id=point.id,
                    todo_id=point.todo_id,
                    author_id=point.author_id,
                    title=point.title,
                    description=point.description,
                    priority=point.priority.name,
                    status=point.status.name,
                    effort_level=(
                        None if point.effort_level is None else point.effort_level.name
                    ),
                    created_at=point.timestamp,
                )
                for todo in todos
                for point in todo.points
            ]
        )

        point_ids_to_check = {
            comment.point_id
            for todo in todos
            for point in todo.points
            for comment in point.comments
        }
        missing_point_ids = point_ids_to_check - {
            value_objects.PointId.from_hex(point_id.hex)
            for point_id in Point.objects.filter(id__in=point_ids_to_check).values_list(
                "id", flat=True
            )
        }
        if missing_point_ids:
            logger.warning(
                "Failed to create todos set, due to missing points with IDs:\n%s",
                pformat(missing_point_ids),
            )
            raise domain_exceptions.PointDoesNotExist(
                f"Points with IDs doesn't exist: \n{pformat(missing_point_ids)}"
            )
        Comment.objects.bulk_create(
            [
                Comment(
                    id=comment.id,
                    point_id=comment.point_id,
                    author_id=comment.author_id,
                    content=comment.content.content,
                    created_at=comment.timestamp,
                )
                for todo in todos
                for point in todo.points
                for comment in point.comments
            ]
        )


class DjangoTodosQueryRepository(query_ports.AbstractTodosQueryRepository):
    """
    See description of parent class to get more details.
    """

    def get(
        self,
        todo_id: value_objects.TodoId,
        executor_id: user_value_objects.USER_ID_TYPE | None = None,
    ) -> query_dtos.OutputTodo:
        query_data = {"id": todo_id}
        if executor_id is not None:
            query_data["executor__id"] = executor_id  # type: ignore[assignment]

        try:
            return map_todo_model_to_output_dto(
                Todo.objects.prefetch_related("points", "author", "executor").get(
                    **query_data
                )
            )
        except Todo.DoesNotExist as err:
            logger.warning(
                "Failed to retrieve todo, due to missing todo with ID '%s' and executor ID '%s'.",
                todo_id,
                executor_id,
            )
            raise domain_exceptions.TodoDoesNotExist(
                f"Todo with ID '{todo_id}' doesn't exist."
            ) from err

    def list(
        self,
        filters: query_ports.TodoFilters,
        ordering: query_ports.TodoOrdering,
        pagination: pagination_dtos.Pagination,
    ) -> tuple[list[query_dtos.OutputTodo], int]:
        query = (
            Todo.objects.prefetch_related("points", "author", "executor")
            .filter(**_get_django_todos_filters(filters))
            .order_by(*_get_django_todos_ordering(ordering))
        )
        return [
            map_todo_model_to_output_dto(todo)
            for todo in query.all()[
                pagination.offset : pagination.offset + pagination.records_per_page
            ]
        ], query.count()


def _get_django_todos_filters(filters: query_ports.TodoFilters) -> dict:
    django_filters: dict[str, Any] = {}

    if filters.ids is not None:
        django_filters["id__in"] = filters.ids
    if filters.author_id is not None:
        django_filters["author_id"] = filters.author_id
    if filters.executor_id is not None:
        django_filters["executor_id"] = filters.executor_id
    if filters.title is not None:
        django_filters["title__icontains"] = filters.title
    if filters.type is not None:
        django_filters["type"] = filters.type.name
    if filters.execute_at_from is not None:
        django_filters["execute_at__gte"] = filters.execute_at_from
    if filters.execute_at_to is not None:
        django_filters["execute_at__lte"] = filters.execute_at_to

    return django_filters


def _get_django_todos_ordering(ordering: query_ports.TodoOrdering) -> list[str]:
    django_ordering: dict[str, ordering_dtos.Ordering] = {}

    if ordering.title is not None:
        django_ordering["title"] = ordering.title
    if ordering.type is not None:
        django_ordering["type"] = ordering.type
    if ordering.execute_at is not None:
        django_ordering["execute_at"] = ordering.execute_at
    if ordering.timestamp is not None:
        django_ordering["created_at"] = ordering.timestamp

    return common_ordering.get_django_ordering(django_ordering)


class DjangoPointsDomainRepository(domain_ports.AbstractPointsDomainRepository):
    """
    See description of parent class to get more details.
    """

    def get(
        self,
        point_id: value_objects.PointId,
        executor_id: user_value_objects.USER_ID_TYPE | None = None,
    ) -> entities.Point:
        query_data = {"id": point_id}
        if executor_id is not None:
            query_data["todo__executor_id"] = executor_id  # type: ignore[assignment]

        try:
            return (
                Point.objects.prefetch_related("todo", "comments", "author")
                .select_for_update()
                .get(**query_data)
                .to_entity()
            )
        except Point.DoesNotExist as err:
            logger.warning(
                "Failed to retrieve point, " "due to missing point with ID '%s'.",
                point_id,
            )
            raise domain_exceptions.PointDoesNotExist(
                f"Point with ID '{point_id}' doesn't exist."
            ) from err

    def create(self, point: entities.Point) -> None:
        todo_id = point.todo_id
        author_id = point.author_id

        try:
            Point.objects.create(
                id=point.id,
                todo=Todo.objects.get(id=todo_id),
                author=User.objects.get(id=author_id),
                title=point.title,
                description=point.description,
                priority=point.priority.name,
                status=point.status.name,
                effort_level=(
                    None if point.effort_level is None else point.effort_level.name
                ),
                created_at=point.timestamp,
            )
        except Todo.DoesNotExist as err:
            logger.warning(
                "Failed to create point, due to missing todo with ID '%s'.",
                todo_id,
            )
            raise domain_exceptions.TodoDoesNotExist(
                f"Todo with ID '{todo_id}' doesn't exist."
            ) from err
        except User.DoesNotExist as err:
            logger.warning(
                "Failed to create point, due to missing author with ID '%s'.",
                author_id,
            )
            raise domain_exceptions.AuthorDoesNotExist(
                f"Author with ID '{author_id}' doesn't exist."
            ) from err

    def update(self, point: entities.Point) -> None:
        point_id = point.id

        try:
            point_ = Point.objects.select_for_update().get(id=point_id)
        except Point.DoesNotExist as err:
            logger.warning(
                "Failed to update point, due to missing point with ID '%s'.",
                point_id,
            )
            raise domain_exceptions.PointDoesNotExist(
                f"Point with ID '{point_id}' doesn't exist."
            ) from err

        point_.title = point.title
        point_.description = point.description
        point_.priority = point.priority.name
        point_.status = point.status.name
        point_.effort_level = (
            None if point.effort_level is None else point.effort_level.name
        )
        point_.save()

    def delete(self, point_id: value_objects.PointId) -> None:
        try:
            Point.objects.get(id=point_id).delete()
        except Point.DoesNotExist as err:
            logger.warning(
                "Failed to delete point, due to missing point with ID '%s'.",
                point_id,
            )
            raise domain_exceptions.PointDoesNotExist(
                f"Point with ID '{point_id}' doesn't exist."
            ) from err


class DjangoPointsQueryRepository(query_ports.AbstractPointsQueryRepository):
    """
    See description of parent class to get more details.
    """

    def get(
        self,
        point_id: value_objects.PointId,
        executor_id: user_value_objects.USER_ID_TYPE | None = None,
    ) -> query_dtos.OutputPoint:
        query_data = {"id": point_id}
        if executor_id is not None:
            query_data["todo__executor__id"] = executor_id  # type: ignore[assignment]

        try:
            return map_point_model_to_output_dto(
                Point.objects.prefetch_related("todo", "comments", "author").get(
                    **query_data
                )
            )
        except Point.DoesNotExist as err:
            logger.warning(
                "Failed to retrieve point, "
                "due to missing point with ID '%s' and assigned to executor '%s'.",
                point_id,
                executor_id,
            )
            raise domain_exceptions.PointDoesNotExist(
                f"Point with ID '{point_id}' doesn't exist."
            ) from err

    def list(
        self,
        filters: query_ports.PointFilters,
        ordering: query_ports.PointOrdering,
        pagination: pagination_dtos.Pagination,
    ) -> tuple[list[query_dtos.OutputPoint], int]:
        query = (
            Point.objects.prefetch_related("todo", "comments", "author")
            .filter(**_get_django_points_filters(filters))
            .order_by(*_get_django_points_ordering(ordering))
        )
        return [
            map_point_model_to_output_dto(point)
            for point in query.all()[
                pagination.offset : pagination.offset + pagination.records_per_page
            ]
        ], query.count()


def _get_django_points_filters(filters: query_ports.PointFilters) -> dict:
    django_filters: dict[str, Any] = {}

    if filters.ids is not None:
        django_filters["id__in"] = filters.ids
    if filters.author_id is not None:
        django_filters["author_id"] = filters.author_id
    if filters.todo_id is not None:
        django_filters["todo_id"] = filters.todo_id
    if filters.executor_id is not None:
        django_filters["todo__executor_id"] = filters.executor_id
    if filters.title is not None:
        django_filters["title__icontains"] = filters.title
    if filters.priority is not None:
        django_filters["priority"] = filters.priority.name
    if filters.status is not None:
        django_filters["status"] = filters.status.name
    if filters.timestamp is not None:
        django_filters["created_at__gte"] = filters.timestamp

    return django_filters


def _get_django_points_ordering(
    ordering: query_ports.PointOrdering,
) -> list[str]:
    django_ordering: dict[str, ordering_dtos.Ordering] = {}

    if ordering.priority is not None:
        django_ordering["priority"] = ordering.priority
    if ordering.timestamp is not None:
        django_ordering["created_at"] = ordering.timestamp

    return common_ordering.get_django_ordering(django_ordering)


class DjangoCommentsDomainRepository(domain_ports.AbstractCommentsDomainRepository):
    """
    See description of parent class to get more details.
    """

    def get(
        self,
        comment_id: value_objects.CommentId,
        owner_id: user_value_objects.USER_ID_TYPE | None = None,
    ) -> entities.Comment:
        query_data = {"id": comment_id}
        if owner_id is not None:
            query_data["point__todo__executor__id"] = owner_id  # type: ignore[assignment]

        try:
            return (
                Comment.objects.select_related("point", "author")
                .select_for_update()
                .get(**query_data)
                .to_entity()
            )
        except Comment.DoesNotExist as err:
            logger.warning(
                "Failed to retrieve comment, " "due to missing comment with ID '%s'.",
                comment_id,
            )
