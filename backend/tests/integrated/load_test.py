#testy adaptera
#todo example of all domain and non-domain integration  test 
# it contains all test cases possible , it contains load query repository and load save operation

#TODO add another test case here, which will test that common test will be raised.

# from datetime import timedelta
# from typing import Any, Callable

# import pytest
# from django.db import transaction

# from infrastructures.apps.todos.adapters import mappers, repositories
# from infrastructures.apps.todos import models
# from modules.common import ordering, pagination
# from modules.todos.domain import (
#     entities,
#     exceptions as domain_exceptions,
#     value_objects,
# )
# from modules.todos.services.queries import dtos as query_dtos, ports as query_ports
# from ...... import entity_factories, fakers as common_fakers, model_factories


# def test_django_todos_domain_repository_get_method_returns_entity_when_record_exists(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()

#     # When
#     with transaction.atomic():
#         result = django_todos_domain_repository.get(todo.id)

#     # Then
#     assert result.id == todo.id
#     assert isinstance(result, entities.Todo)


# def test_django_todos_domain_repository_get_method_raises_exception_when_record_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     todo_id = common_fakers.fake_todo_id()

#     # When and then
#     with pytest.raises(domain_exceptions.TodoDoesNotExist), transaction.atomic():
#         django_todos_domain_repository.get(todo_id)


# def test_django_todos_domain_repository_create_method_creates_record(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     user_id = model_factories.UserFactory.create().id
#     todo_entity = entity_factories.TodoEntityFactory.create(
#         author_id=user_id,
#         executor_id=user_id,
#     )

#     # When
#     django_todos_domain_repository.create(todo_entity)

#     # Then
#     assert models.Todo.objects.filter(id=todo_entity.id).count() == 1


# def test_django_todos_domain_repository_raises_exception_when_author_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     user_id = model_factories.UserFactory.create().id
#     todo_entity = entity_factories.TodoEntityFactory.create(
#         author_id=common_fakers.fake_user_id(),
#         executor_id=user_id,
#     )

#     # When and then
#     with pytest.raises(domain_exceptions.AuthorDoesNotExist), transaction.atomic():
#         django_todos_domain_repository.create(todo_entity)


# def test_django_todos_domain_repository_raises_exception_when_executor_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     user_id = model_factories.UserFactory.create().id
#     todo_entity = entity_factories.TodoEntityFactory.create(
#         author_id=user_id,
#         executor_id=common_fakers.fake_user_id(),
#     )

#     # When and then
#     with pytest.raises(domain_exceptions.ExecutorDoesNotExist), transaction.atomic():
#         django_todos_domain_repository.create(todo_entity)


# @pytest.mark.parametrize(
#     ("attribute", "value"),
#     (
#         ("title", common_fakers.fake_title()),
#         ("description", common_fakers.fake_description()),
#         (
#             "type",
#             common_fakers.fake_todo_type().name,
#         ),
#         (
#             "execute_at",
#             common_fakers.fake_timestamp(),
#         ),
#     ),
# )
# def test_django_todos_domain_repository_update_method_updates_record(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
#     attribute: str,
#     value: Any,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create(
#         **{attribute: value},
#     )

#     # When
#     with transaction.atomic():
#         django_todos_domain_repository.update(todo.to_entity())

#     # Then
#     updated_todo = models.Todo.objects.get(id=todo.id)
#     assert getattr(updated_todo, attribute) == value


# def test_django_todos_domain_repository_update_method_updates_executor_field(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     new_executor = model_factories.UserFactory.create()
#     todo = model_factories.TodoFactory.create(
#         type=value_objects.TodoType.TRAINING.name,
#     )
#     todo_entity = todo.to_entity()
#     todo_entity.executor_id = new_executor.id

#     # When
#     with transaction.atomic():
#         django_todos_domain_repository.update(todo_entity)

#     # Then
#     assert models.Todo.objects.get(id=todo.id).executor == new_executor


# @pytest.mark.parametrize(
#     ("attribute", "value"),
#     (("author_id", common_fakers.fake_user_id()),),
# )
# def test_django_todos_domain_repository_update_method_updates_only_expected_fields(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
#     attribute: str,
#     value: Any,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     todo_entity = todo.to_entity()
#     setattr(todo_entity, attribute, value)

#     # When
#     with transaction.atomic():
#         django_todos_domain_repository.update(todo_entity)

#     # Then
#     assert getattr(models.Todo.objects.get(id=todo.id), attribute) == getattr(
#         todo, attribute
#     )


# def test_django_todos_domain_repository_update_method_raises_exception_when_record_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     todo.id = common_fakers.fake_todo_id()

#     # When and then
#     with pytest.raises(domain_exceptions.TodoDoesNotExist), transaction.atomic():
#         django_todos_domain_repository.update(todo.to_entity())


# def test_django_todos_domain_repository_delete_method_deletes_record(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()

#     # When
#     django_todos_domain_repository.delete(todo.id)

#     # Then
#     assert not models.Todo.objects.filter(id=todo.id).exists()


# def test_django_todos_domain_repository_delete_method_raises_exception_when_record_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     todo_id = common_fakers.fake_todo_id()

#     # When and then
#     with pytest.raises(domain_exceptions.TodoDoesNotExist):
#         django_todos_domain_repository.delete(todo_id)


# def test_django_todos_domain_repository_creates_set_method_creates_records(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     author = model_factories.UserFactory.create()
#     executor = model_factories.UserFactory.create()

#     records_number = 5
#     todos = entity_factories.TodoEntityFactory.create_batch(
#         size=records_number, author_id=author.id, executor_id=executor.id
#     )
#     for todo in todos:
#         for _ in range(records_number):
#             point = entity_factories.PointEntityFactory.create(
#                 todo_id=todo.id, author_id=author.id, executor_id=executor.id
#             )
#             for _ in range(records_number):
#                 point.comments.append(
#                     entity_factories.CommentEntityFactory.create(
#                         point_id=point.id, author_id=author.id
#                     )
#                 )
#             todo.points.append(point)

#     # When
#     django_todos_domain_repository.create_set(todos)

#     # Then
#     assert (
#         models.Todo.objects.filter(id__in=[todo.id for todo in todos]).count()
#         == records_number
#     )
#     assert (
#         models.Point.objects.filter(todo_id__in=[todo.id for todo in todos]).count()
#         == records_number * records_number
#     )
#     assert (
#         models.Comment.objects.filter(
#             point_id__in=[point.id for todo in todos for point in todo.points]
#         ).count()
#         == records_number * records_number * records_number
#     )
#     assert all(todo.author_id == author.id for todo in todos)
#     assert all(todo.executor_id == executor.id for todo in todos)
#     assert all(point.author_id == author.id for todo in todos for point in todo.points)
#     assert all(
#         comment.author_id == author.id
#         for todo in todos
#         for point in todo.points
#         for comment in point.comments
#     )
#     assert all(
#         models.Point.objects.filter(todo_id=todo.id).count() == records_number
#         for todo in todos
#     )
#     assert all(
#         models.Comment.objects.filter(point_id=point.id).count() == records_number
#         for todo in todos
#         for point in todo.points
#     )


# def test_django_todos_domain_repository_creates_set_raises_exception_when_todo_author_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     executor = model_factories.UserFactory.create()
#     todo = entity_factories.TodoEntityFactory.create(
#         executor_id=executor.id,
#     )

#     # When and then
#     with pytest.raises(domain_exceptions.AuthorDoesNotExist):
#         django_todos_domain_repository.create_set([todo])

#     assert not models.Todo.objects.exists()
#     assert not models.Point.objects.exists()
#     assert not models.Comment.objects.exists()


# def test_django_todos_domain_repository_creates_set_raises_exception_when_todo_executor_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     author = model_factories.UserFactory.create()
#     todo = entity_factories.TodoEntityFactory.create(
#         author_id=author.id,
#     )

#     # When and then
#     with pytest.raises(domain_exceptions.ExecutorDoesNotExist):
#         django_todos_domain_repository.create_set([todo])

#     assert not models.Todo.objects.exists()
#     assert not models.Point.objects.exists()
#     assert not models.Comment.objects.exists()


# def test_django_todos_domain_repository_creates_set_raises_exception_when_point_author_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     user = model_factories.UserFactory.create()
#     todo = entity_factories.TodoEntityFactory.create(
#         author_id=user.id, executor_id=user.id
#     )
#     todo.points.append(entity_factories.PointEntityFactory.create(todo_id=todo.id))

#     # When and then
#     with pytest.raises(domain_exceptions.AuthorDoesNotExist):
#         django_todos_domain_repository.create_set([todo])

#     assert not models.Todo.objects.exists()
#     assert not models.Point.objects.exists()
#     assert not models.Comment.objects.exists()


# def test_django_todos_domain_repository_creates_set_raises_exception_when_comment_author_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     user = model_factories.UserFactory.create()
#     todo = entity_factories.TodoEntityFactory.create(
#         author_id=user.id, executor_id=user.id
#     )
#     point = entity_factories.PointEntityFactory.create(
#         todo_id=todo.id, author_id=user.id
#     )
#     comment = entity_factories.CommentEntityFactory.create(point_id=point.id)
#     point.comments.append(comment)
#     todo.points.append(point)

#     # When and then
#     with pytest.raises(domain_exceptions.AuthorDoesNotExist):
#         django_todos_domain_repository.create_set([todo])

#     assert not models.Todo.objects.exists()
#     assert not models.Point.objects.exists()
#     assert not models.Comment.objects.exists()


# def test_django_todos_domain_repository_creates_set_raises_exception_when_point_todo_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     author = model_factories.UserFactory.create()
#     todo = entity_factories.TodoEntityFactory.create(
#         author_id=author.id, executor_id=model_factories.UserFactory.create().id
#     )
#     todo.points.append(entity_factories.PointEntityFactory.create(author_id=author.id))

#     # When and then
#     with pytest.raises(domain_exceptions.TodoDoesNotExist):
#         django_todos_domain_repository.create_set([todo])

#     assert not models.Todo.objects.exists()
#     assert not models.Point.objects.exists()
#     assert not models.Comment.objects.exists()


# def test_django_todos_domain_repository_creates_set_raises_exception_when_comment_point_does_not_exist(
#     django_todos_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     author = model_factories.UserFactory.create()
#     todo = entity_factories.TodoEntityFactory.create(
#         author_id=author.id, executor_id=model_factories.UserFactory.create().id
#     )
#     point = entity_factories.PointEntityFactory.create(
#         todo_id=todo.id, author_id=author.id
#     )
#     point.comments.append(
#         entity_factories.CommentEntityFactory.create(author_id=author.id)
#     )
#     todo.points.append(point)

#     # When and then
#     with pytest.raises(domain_exceptions.PointDoesNotExist):
#         django_todos_domain_repository.create_set([todo])

#     assert not models.Todo.objects.all()
#     assert not models.Point.objects.exists()
#     assert not models.Comment.objects.exists()


# def test_django_points_domain_repository_get_method_returns_entity_when_record_exists(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()

#     # When
#     with transaction.atomic():
#         result = django_points_domain_repository.get(point.id)

#     # Then
#     assert result.id == point.id
#     assert isinstance(result, entities.Point)


# def test_django_points_domain_repository_get_method_raises_exception_when_record_does_not_exist(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
# ):
#     # Given
#     point_id = common_fakers.fake_point_id()

#     # When and then
#     with pytest.raises(domain_exceptions.PointDoesNotExist), transaction.atomic():
#         django_points_domain_repository.get(point_id)


# def test_django_points_domain_repository_create_method_creates_record(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     point_entity = entity_factories.PointEntityFactory.create(
#         todo_id=todo.id,
#         author_id=todo.executor.id,
#     )

#     # When
#     django_points_domain_repository.create(point_entity)

#     # Then
#     assert models.Point.objects.filter(id=point_entity.id).count() == 1


# def test_django_points_domain_repository_create_method_raises_exception_author_does_not_exist(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     point_entity = entity_factories.PointEntityFactory.create(
#         todo_id=todo.id,
#     )

#     # When and then
#     with pytest.raises(domain_exceptions.AuthorDoesNotExist):
#         django_points_domain_repository.create(point_entity)

#     assert not models.Point.objects.exists()


# def test_django_points_domain_repository_create_method_raises_exception_when_todo_does_not_exist(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
# ):
#     # Given
#     author = model_factories.UserFactory.create()
#     point_entity = entity_factories.PointEntityFactory.create(
#         author_id=author.id,
#     )

#     # When and then
#     with pytest.raises(domain_exceptions.TodoDoesNotExist):
#         django_points_domain_repository.create(point_entity)

#     assert not models.Point.objects.exists()


# @pytest.mark.parametrize(
#     ("attribute", "value"),
#     (
#         ("title", common_fakers.fake_title()),
#         ("description", common_fakers.fake_description()),
#         (
#             "priority",
#             common_fakers.fake_point_priority(
#                 exclude=value_objects.PointPriority.LOW
#             ).name,
#         ),
#         (
#             "status",
#             common_fakers.fake_point_status(
#                 exclude=value_objects.PointStatus.TO_FOLLOW
#             ).name,
#         ),
#         (
#             "effort_level",
#             common_fakers.fake_point_effort_level(
#                 exclude=value_objects.PointEffortLevel.EASY
#             ).name,
#         ),
#     ),
# )
# def test_django_points_domain_repository_update_method_updates_record(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
#     attribute: str,
#     value: Any,
# ):
#     # Given
#     point = model_factories.PointFactory.create(
#         **{attribute: value},
#     )

#     # When
#     with transaction.atomic():
#         django_points_domain_repository.update(point.to_entity())

#     # Then
#     updated_point = models.Point.objects.get(id=point.id)
#     assert getattr(updated_point, attribute) == value


# @pytest.mark.parametrize(
#     ("attribute", "value"),
#     (
#         ("todo_id", common_fakers.fake_todo_id()),
#         ("author_id", common_fakers.fake_user_id()),
#     ),
# )
# def test_django_points_domain_repository_update_method_updates_only_expected_fields(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
#     attribute: str,
#     value: Any,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     point_entity = point.to_entity()
#     setattr(point_entity, attribute, value)

#     # When
#     with transaction.atomic():
#         django_points_domain_repository.update(point_entity)

#     # Then
#     assert getattr(models.Point.objects.get(id=point.id), attribute) == getattr(
#         point, attribute
#     )


# def test_django_points_domain_repository_update_method_raises_exception_when_record_does_not_exist(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     point.id = common_fakers.fake_point_id()

#     # When and then
#     with pytest.raises(domain_exceptions.PointDoesNotExist), transaction.atomic():
#         django_points_domain_repository.update(point.to_entity())


# def test_django_points_domain_repository_delete_method_deletes_record(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()

#     # When
#     django_points_domain_repository.delete(point.id)

#     # Then
#     assert not models.Point.objects.filter(id=point.id).exists()


# def test_django_points_domain_repository_delete_method_raises_exception_when_record_does_not_exist(
#     django_points_domain_repository: repositories.DjangoPointsDomainRepository,
# ):
#     # Given
#     point_id = common_fakers.fake_point_id()

#     # When and then
#     with pytest.raises(domain_exceptions.PointDoesNotExist):
#         django_points_domain_repository.delete(point_id)


# def test_django_comments_domain_repository_get_method_returns_entity_when_record_exists(
#     django_comments_domain_repository: repositories.DjangoCommentsDomainRepository,
# ):
#     # Given
#     comment = model_factories.CommentFactory.create()

#     # When
#     with transaction.atomic():
#         result = django_comments_domain_repository.get(comment.id)

#     # Then
#     assert result.id == comment.id
#     assert isinstance(result, entities.Comment)


# def test_django_comments_domain_repository_get_method_raises_exception_when_record_does_not_exist(
#     django_comments_domain_repository: repositories.DjangoTodosDomainRepository,
# ):
#     # Given
#     todo_id = common_fakers.fake_todo_id()

#     # When and then
#     with pytest.raises(domain_exceptions.CommentDoesNotExist), transaction.atomic():
#         django_comments_domain_repository.get(todo_id)


# def test_django_comments_domain_repository_create_method_creates_record(
#     django_comments_domain_repository: repositories.DjangoCommentsDomainRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     comment_entity = entity_factories.CommentEntityFactory.create(
#         point_id=point.id,
#         author_id=point.author.id,
#     )

#     # When
#     django_comments_domain_repository.create(comment_entity)

#     # Then
#     assert models.Comment.objects.filter(id=comment_entity.id).count() == 1


# def test_django_comments_domain_repository_create_method_raises_exception_author_does_not_exist(
#     django_comments_domain_repository: repositories.DjangoCommentsDomainRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     comment_entity = entity_factories.CommentEntityFactory.create(
#         point_id=point.id,
#     )

#     # When and then
#     with pytest.raises(domain_exceptions.AuthorDoesNotExist):
#         django_comments_domain_repository.create(comment_entity)

#     assert not models.Comment.objects.exists()


# def test_django_comments_domain_repository_create_method_raises_exception_point_does_not_exist(
#     django_comments_domain_repository: repositories.DjangoCommentsDomainRepository,
# ):
#     # Given
#     author = model_factories.UserFactory.create()
#     comment_entity = entity_factories.CommentEntityFactory.create(
#         author_id=author.id,
#     )

#     # When and then
#     with pytest.raises(domain_exceptions.PointDoesNotExist):
#         django_comments_domain_repository.create(comment_entity)

#     assert not models.Comment.objects.exists()


# @pytest.mark.parametrize(
#     ("attribute", "value"), (("content", common_fakers.fake_content()),)
# )
# def test_django_comments_domain_repository_update_method_updates_record(
#     django_comments_domain_repository: repositories.DjangoCommentsDomainRepository,
#     attribute: str,
#     value: Any,
# ):
#     # Given
#     comment = model_factories.CommentFactory.create(
#         **{attribute: value},
#     )

#     # When
#     with transaction.atomic():
#         django_comments_domain_repository.update(comment.to_entity())

#     # Then
#     updated_comment = models.Comment.objects.get(id=comment.id)
#     assert getattr(updated_comment, attribute) == value


# @pytest.mark.parametrize(
#     ("attribute", "value"),
#     (
#         ("point_id", common_fakers.fake_todo_id()),
#         ("author_id", common_fakers.fake_user_id()),
#     ),
# )
# def test_django_comments_domain_repository_update_method_updates_only_expected_fields(
#     django_comments_domain_repository: repositories.DjangoCommentsDomainRepository,
#     attribute: str,
#     value: Any,
# ):
#     # Given
#     comment = model_factories.CommentFactory.create()
#     comment_entity = comment.to_entity()
#     setattr(comment_entity, attribute, value)

#     # When
#     with transaction.atomic():
#         django_comments_domain_repository.update(comment_entity)

#     # Then
#     assert getattr(models.Comment.objects.get(id=comment.id), attribute) == getattr(
#         comment, attribute
#     )


# def test_django_comments_domain_repository_update_method_raises_exception_when_record_does_not_exist(
#     django_comments_domain_repository: repositories.DjangoCommentsDomainRepository,
# ):
#     # Given
#     comment = model_factories.CommentFactory.create()
#     comment.id = common_fakers.fake_comment_id()

#     # When and then
#     with pytest.raises(domain_exceptions.CommentDoesNotExist), transaction.atomic():
#         django_comments_domain_repository.update(comment.to_entity())


# def test_django_comments_domain_repository_delete_method_deletes_record(
#     django_comments_domain_repository: repositories.DjangoCommentsDomainRepository,
# ):
#     # Given
#     comment = model_factories.CommentFactory.create()

#     # When
#     django_comments_domain_repository.delete(comment.id)

#     # Then
#     assert not models.Comment.objects.filter(id=comment.id).exists()


# def test_django_comments_domain_repository_delete_method_raises_exception_when_record_does_not_exist(
#     django_comments_domain_repository: repositories.DjangoCommentsDomainRepository,
# ):
#     # Given
#     comment_id = common_fakers.fake_comment_id()

#     # When and then
#     with pytest.raises(domain_exceptions.CommentDoesNotExist):
#         django_comments_domain_repository.delete(comment_id)


# def test_todos_query_repository_get_method_returns_output_dto_when_record_exists(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()

#     # When
#     result = django_todos_query_repository.get(todo.id)

#     # Then
#     assert result.id == todo.id
#     assert isinstance(result, query_dtos.OutputTodo)


# def test_todos_query_repository_get_method_raises_exception_when_record_does_not_exist(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # Given
#     todo_id = common_fakers.fake_todo_id()

#     # When and then
#     with pytest.raises(domain_exceptions.TodoDoesNotExist):
#         django_todos_query_repository.get(todo_id)


# def test_todos_query_repository_list_method_returns_output_dtos_when_records_exist(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # Given
#     todos_number = 3
#     model_factories.TodoFactory.create_batch(todos_number)

#     # When
#     results, count = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(),
#         ordering=query_ports.TodoOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=todos_number,
#         ),
#     )

#     # Then
#     assert count == todos_number
#     assert isinstance(results, list)
#     assert all(isinstance(todo, query_dtos.OutputTodo) for todo in results)


# def test_todos_query_repository_list_method_returns_empty_list_when_no_records(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # When
#     results, count = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(),
#         ordering=query_ports.TodoOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 0
#     assert isinstance(results, list)
#     assert not results


# def test_todos_query_repository_list_method_filters_by_ids(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     model_factories.TodoFactory.create()

#     # When
#     results, count = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(
#             ids=[todo.id],
#         ),
#         ordering=query_ports.TodoOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == todo.id


# def test_todos_query_repository_list_method_filters_by_author_id(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     model_factories.TodoFactory.create()

#     # When
#     results, count = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(
#             author_id=todo.author.id,
#         ),
#         ordering=query_ports.TodoOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == todo.id


# def test_todos_query_repository_list_method_filters_by_executor_id(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     model_factories.TodoFactory.create()

#     # When
#     results, count = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(
#             executor_id=todo.executor.id,
#         ),
#         ordering=query_ports.TodoOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == todo.id


# @pytest.mark.parametrize(
#     ("attribute", "value_modifier"),
#     [
#         ("title", str.upper),
#         ("title", str.lower),
#     ],
# )
# def test_todos_query_repository_list_method_filters_by_case_insensitive_values(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
#     attribute: str,
#     value_modifier: Callable,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     model_factories.TodoFactory.create()

#     # When
#     results, count = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(
#             **{attribute: value_modifier(getattr(todo, attribute))}
#         ),
#         ordering=query_ports.TodoOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == todo.id


# def test_todos_query_repository_list_method_filters_by_type(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     model_factories.TodoFactory.create(
#         type=common_fakers.fake_todo_type(exclude=value_objects.TodoType[todo.type])
#     )

#     # When
#     results, count = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(
#             type=value_objects.TodoType[todo.type],
#         ),
#         ordering=query_ports.TodoOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == todo.id


# def test_todos_query_repository_list_method_filters_by_execute_at_from(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     model_factories.TodoFactory.create(
#         execute_at=todo.execute_at - timedelta(seconds=1)
#     )

#     # When
#     results, count = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(execute_at_from=todo.execute_at),
#         ordering=query_ports.TodoOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == todo.id


# def test_todos_query_repository_list_method_filters_by_execute_at_to(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
# ):
#     # Given
#     todo = model_factories.TodoFactory.create()
#     model_factories.TodoFactory.create(
#         execute_at=todo.execute_at + timedelta(seconds=1)
#     )

#     # When
#     results, count = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(execute_at_to=todo.execute_at),
#         ordering=query_ports.TodoOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == todo.id


# @pytest.mark.parametrize(
#     "order_by",
#     (
#         "title",
#         "-title",
#         "type",
#         "-type",
#         "execute_at",
#         "-execute_at",
#     ),
# )
# def test_django_todos_query_repository_list_method_ordering(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
#     order_by: str,
# ):
#     # Given
#     model_factories.TodoFactory.create_batch(size=5)

#     # When
#     results, _ = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(),
#         ordering=query_ports.TodoOrdering(
#             **{
#                 (
#                     order_by[1:] if order_by.startswith("-") else order_by
#                 ): ordering.Ordering(
#                     order=(
#                         ordering.OrderingOrder.DESCENDING
#                         if order_by.startswith("-")
#                         else ordering.OrderingOrder.ASCENDING
#                     ),
#                     priority=1,
#                 )
#             }
#         ),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert results == [
#         mappers.map_todo_model_to_output_dto(todo)
#         for todo in models.Todo.objects.order_by(order_by)
#     ]


# @pytest.mark.parametrize(
#     "order_by",
#     (
#         "timestamp",
#         "-timestamp",
#     ),
# )
# def test_django_todos_query_repository_list_method_ordering_by_timestamp(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
#     order_by: str,
# ):
#     # Given
#     model_factories.TodoFactory.create_batch(size=5)

#     # When
#     results, _ = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(),
#         ordering=query_ports.TodoOrdering(
#             **{
#                 (
#                     order_by[1:] if order_by.startswith("-") else order_by
#                 ): ordering.Ordering(
#                     order=(
#                         ordering.OrderingOrder.DESCENDING
#                         if order_by.startswith("-")
#                         else ordering.OrderingOrder.ASCENDING
#                     ),
#                     priority=1,
#                 )
#             }
#         ),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert results == [
#         mappers.map_todo_model_to_output_dto(todo)
#         for todo in models.Todo.objects.order_by(
#             f"{'-' if order_by.startswith('-') else ''}created_at"
#         )
#     ]


# @pytest.mark.parametrize("orders_by", (("type", "title"), ("type", "-title")))
# def test_django_todos_query_repository_list_method_ordering_by_a_few_attributes(
#     django_todos_query_repository: repositories.DjangoTodosQueryRepository,
#     orders_by: str,
# ):
#     # Given
#     model_factories.TodoFactory.create_batch(size=5)
#     ordering_ = {}
#     for index, order_by in enumerate(orders_by):
#         ordering_[order_by[1:] if order_by.startswith("-") else order_by] = (
#             ordering.Ordering(
#                 order=(
#                     ordering.OrderingOrder.DESCENDING
#                     if order_by.startswith("-")
#                     else ordering.OrderingOrder.ASCENDING
#                 ),
#                 priority=index + 1,
#             )
#         )

#     # When
#     results, _ = django_todos_query_repository.list(
#         filters=query_ports.TodoFilters(),
#         ordering=query_ports.TodoOrdering(**ordering_),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert results == [
#         mappers.map_todo_model_to_output_dto(todo)
#         for todo in models.Todo.objects.order_by(*orders_by)
#     ]


# def test_django_points_query_repository_get_method_returns_output_dto_when_record_exists(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()

#     # When
#     result = django_points_query_repository.get(point.id)

#     # Then
#     assert result.id == point.id
#     assert isinstance(result, query_dtos.OutputPoint)


# def test_django_points_query_repository_get_method_raises_exception_when_record_does_not_exist(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     point_id = common_fakers.fake_point_id()

#     # When and then
#     with pytest.raises(domain_exceptions.PointDoesNotExist):
#         django_points_query_repository.get(point_id)


# def test_points_query_repository_list_method_returns_output_dtos_when_records_exist(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     points_number = 3
#     model_factories.PointFactory.create_batch(points_number)

#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=points_number,
#         ),
#     )

#     # Then
#     assert count == points_number
#     assert isinstance(results, list)
#     assert all(isinstance(point, query_dtos.OutputPoint) for point in results)


# def test_points_query_repository_list_method_returns_empty_list_when_no_records(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 0
#     assert isinstance(results, list)
#     assert not results


# def test_points_query_repository_list_method_filters_by_ids(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     model_factories.PointFactory.create()

#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(
#             ids=[point.id],
#         ),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == point.id


# def test_points_query_repository_list_method_filters_author_id(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     model_factories.PointFactory.create()

#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(
#             author_id=point.author.id,
#         ),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == point.id


# def test_points_query_repository_list_method_filters_todo_id(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     model_factories.PointFactory.create()

#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(
#             todo_id=point.todo.id,
#         ),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == point.id


# def test_points_query_repository_list_method_filters_executor_id(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     model_factories.PointFactory.create()

#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(
#             executor_id=point.todo.executor.id,
#         ),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == point.id


# @pytest.mark.parametrize(
#     ("attribute", "value_modifier"),
#     [
#         ("title", str.upper),
#         ("title", str.lower),
#     ],
# )
# def test_points_query_repository_list_method_filters_by_case_insensitive_values(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
#     attribute: str,
#     value_modifier: Callable,
# ):
#     # Given
#     todo = model_factories.PointFactory.create()
#     model_factories.PointFactory.create()

#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(
#             **{attribute: value_modifier(getattr(todo, attribute))}
#         ),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == todo.id


# def test_points_query_repository_list_method_filters_by_priority(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     model_factories.PointFactory.create(
#         priority=common_fakers.fake_point_priority(
#             exclude=value_objects.PointPriority[point.priority]
#         )
#     )

#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(
#             priority=value_objects.PointPriority[point.priority],
#         ),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == point.id


# def test_points_query_repository_list_method_filters_by_status(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     point = model_factories.PointFactory.create()
#     model_factories.PointFactory.create(
#         status=common_fakers.fake_point_status(
#             exclude=value_objects.PointStatus[point.status]
#         )
#     )

#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(
#             status=value_objects.PointStatus[point.status],
#         ),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == point.id


# def test_points_query_repository_list_method_filters_by_timestamp(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
# ):
#     # Given
#     model_factories.PointFactory.create()
#     point = model_factories.PointFactory.create()

#     # When
#     results, count = django_points_query_repository.list(
#         filters=query_ports.PointFilters(
#             timestamp=point.created_at,
#         ),
#         ordering=query_ports.PointOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == point.id


# @pytest.mark.parametrize(
#     "order_by",
#     (
#         "priority",
#         "-priority",
#     ),
# )
# def test_django_points_query_repository_list_method_ordering(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
#     order_by: str,
# ):
#     # Given
#     model_factories.PointFactory.create_batch(size=5)

#     # When
#     results, _ = django_points_query_repository.list(
#         filters=query_ports.PointFilters(),
#         ordering=query_ports.PointOrdering(
#             **{
#                 (
#                     order_by[1:] if order_by.startswith("-") else order_by
#                 ): ordering.Ordering(
#                     order=(
#                         ordering.OrderingOrder.DESCENDING
#                         if order_by.startswith("-")
#                         else ordering.OrderingOrder.ASCENDING
#                     ),
#                     priority=1,
#                 )
#             }
#         ),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert results == [
#         mappers.map_point_model_to_output_dto(point)
#         for point in models.Point.objects.order_by(order_by)
#     ]


# @pytest.mark.parametrize("order_by", ("timestamp", "-timestamp"))
# def test_django_points_query_repository_list_method_ordering_by_timestamp(
#     django_points_query_repository: repositories.DjangoPointsQueryRepository,
#     order_by: str,
# ):
#     # Given
#     model_factories.PointFactory.create_batch(size=5)

#     # When
#     results, _ = django_points_query_repository.list(
#         filters=query_ports.PointFilters(),
#         ordering=query_ports.PointOrdering(
#             **{
#                 (
#                     order_by[1:] if order_by.startswith("-") else order_by
#                 ): ordering.Ordering(
#                     order=(
#                         ordering.OrderingOrder.DESCENDING
#                         if order_by.startswith("-")
#                         else ordering.OrderingOrder.ASCENDING
#                     ),
#                     priority=1,
#                 )
#             }
#         ),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert results == [
#         mappers.map_point_model_to_output_dto(point)
#         for point in models.Point.objects.order_by(
#             f"{'-' if order_by.startswith('-') else ''}created_at"
#         )
#     ]


# def test_django_comments_query_repository_get_method_returns_output_dto_when_record_exists(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
# ):
#     # Given
#     comment = model_factories.CommentFactory.create()

#     # When
#     result = django_comments_query_repository.get(comment.id)

#     # Then
#     assert result.id == comment.id
#     assert isinstance(result, query_dtos.OutputComment)


# def test_django_comments_query_repository_get_method_raises_exception_when_record_does_not_exist(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
# ):
#     # Given
#     comment_id = common_fakers.fake_comment_id()

#     # When and then
#     with pytest.raises(domain_exceptions.CommentDoesNotExist):
#         django_comments_query_repository.get(comment_id)


# def test_comments_query_repository_list_method_returns_output_dtos_when_records_exist(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
# ):
#     # Given
#     comments_number = 3
#     model_factories.CommentFactory.create_batch(comments_number)

#     # When
#     results, count = django_comments_query_repository.list(
#         filters=query_ports.CommentFilters(),
#         ordering=query_ports.CommentOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=comments_number,
#         ),
#     )

#     # Then
#     assert count == comments_number
#     assert isinstance(results, list)
#     assert all(isinstance(comment, query_dtos.OutputComment) for comment in results)


# def test_comments_query_repository_list_method_returns_empty_list_when_no_records(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
# ):
#     # When
#     results, count = django_comments_query_repository.list(
#         filters=query_ports.CommentFilters(),
#         ordering=query_ports.CommentOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 0
#     assert isinstance(results, list)
#     assert not results


# def test_comments_query_repository_list_method_filters_by_ids(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
# ):
#     # Given
#     comment = model_factories.CommentFactory.create()
#     model_factories.CommentFactory.create()

#     # When
#     results, count = django_comments_query_repository.list(
#         filters=query_ports.CommentFilters(
#             ids=[comment.id],
#         ),
#         ordering=query_ports.CommentOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == comment.id


# def test_comments_query_repository_list_method_filters_author_id(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
# ):
#     # Given
#     comment = model_factories.CommentFactory.create()
#     model_factories.CommentFactory.create()

#     # When
#     results, count = django_comments_query_repository.list(
#         filters=query_ports.CommentFilters(
#             author_id=comment.author.id,
#         ),
#         ordering=query_ports.CommentOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == comment.id


# def test_comments_query_repository_list_method_filters_point_id(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
# ):
#     # Given
#     comment = model_factories.CommentFactory.create()
#     model_factories.CommentFactory.create()

#     # When
#     results, count = django_comments_query_repository.list(
#         filters=query_ports.CommentFilters(
#             point_id=comment.point.id,
#         ),
#         ordering=query_ports.CommentOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == comment.id


# @pytest.mark.parametrize(
#     ("attribute", "value_modifier"),
#     [
#         ("content", str.upper),
#         ("content", str.lower),
#     ],
# )
# def test_comments_query_repository_list_method_filters_by_case_insensitive_values(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
#     attribute: str,
#     value_modifier: Callable,
# ):
#     # Given
#     point = model_factories.CommentFactory.create()
#     model_factories.CommentFactory.create()

#     # When
#     results, count = django_comments_query_repository.list(
#         filters=query_ports.CommentFilters(
#             **{attribute: value_modifier(getattr(point, attribute))}
#         ),
#         ordering=query_ports.CommentOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == point.id


# def test_comments_query_repository_list_method_filters_by_timestamp(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
# ):
#     # Given
#     model_factories.CommentFactory.create()
#     comment = model_factories.CommentFactory.create()

#     # When
#     results, count = django_comments_query_repository.list(
#         filters=query_ports.CommentFilters(
#             timestamp=comment.created_at,
#         ),
#         ordering=query_ports.CommentOrdering(),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert count == 1
#     assert results[0].id == comment.id


# @pytest.mark.parametrize("order_by", ("timestamp", "-timestamp"))
# def test_django_comments_query_repository_list_method_ordering_by_timestamp(
#     django_comments_query_repository: repositories.DjangoCommentsQueryRepository,
#     order_by: str,
# ):
#     # Given
#     model_factories.CommentFactory.create_batch(size=5)

#     # When
#     results, _ = django_comments_query_repository.list(
#         filters=query_ports.CommentFilters(),
#         ordering=query_ports.CommentOrdering(
#             **{
#                 (
#                     order_by[1:] if order_by.startswith("-") else order_by
#                 ): ordering.Ordering(
#                     order=(
#                         ordering.OrderingOrder.DESCENDING
#                         if order_by.startswith("-")
#                         else ordering.OrderingOrder.ASCENDING
#                     ),
#                     priority=1,
#                 )
#             }
#         ),
#         pagination=pagination.Pagination(
#             offset=pagination.PAGINATION_DEFAULT_OFFSET,
#             records_per_page=pagination.PAGINATION_DEFAULT_LIMIT,
#         ),
#     )

#     # Then
#     assert results == [
#         mappers.map_comment_model_to_output_dto(comment)
#         for comment in models.Comment.objects.order_by(
#             f"{'-' if order_by.startswith('-') else ''}created_at"
#         )
#     ]
