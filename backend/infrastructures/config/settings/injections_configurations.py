import inspect
from collections import defaultdict
from typing import Callable

import inject
from django.conf import settings

from infrastructures.common.adapters import task_dispatchers
from infrastructures.apps.courses import adapters as course_adapters
from infrastructures.apps.events import adapters as event_adapters
from infrastructures.apps.locations import adapters as location_adapters
from infrastructures.apps.notifications import adapters as notification_adapters
from infrastructures.apps.payments import adapters as payment_adapters
from infrastructures.apps.planner import adapters as planner_adapters
from infrastructures.apps.todos import adapters as todo_adapters
from infrastructures.apps.users import adapters as user_adapters
from modules.common import message_bus
from modules.common.domain import events as common_events
from modules.courses.services import handlers as course_handlers
from modules.events.services import handlers as event_handlers
from modules.planner.services import handlers as planner_handlers
from modules.todos.services import handlers as todo_handlers



def inject_config(binder: inject.Binder):
    binder.bind_to_constructor(
        "email_notificator",
        notification_adapters.DjangoEmailNotificator,
    )
    binder.bind_to_constructor(
        "comments_query_repository",
        todo_adapters.DjangoCommentsQueryRepository,
    )
    binder.bind_to_constructor(
        "courses_query_repository", course_adapters.DjangoCoursesQueryRepository
    )
    binder.bind_to_constructor(
        "courses_unit_of_work", course_adapters.DjangoCoursesUnitOfWork
    )
    binder.bind_to_constructor(
        "events_query_repository", event_adapters.DjangoEventsQueryRepository
    )
    binder.bind_to_constructor(
        "events_unit_of_work", event_adapters.DjangoEventsUnitOfWork
    )
    binder.bind_to_constructor(
        "locations_query_repository",
        location_adapters.DjangoLocationsQueryRepository,
    )
    binder.bind_to_constructor(
        "orders_query_repository",
        payment_adapters.DjangoOrdersQueryRepository,
    )
    binder.bind_to_constructor(
        "reservations_query_repository",
        event_adapters.DjangoReservationsQueryRepository,
    )
    binder.bind_to_provider(
        "payments_gateway",
        lambda: payment_adapters.Przelewy24PaymentsGateway(
            mode=settings.PRZELEWY24_CONFIG["MODE"],  # type: ignore[arg-type]
            pos_id=settings.PRZELEWY24_CONFIG["POS_ID"],  # type: ignore[arg-type]
            merchant_id=settings.PRZELEWY24_CONFIG["MERCHANT_ID"],  # type: ignore[arg-type]
            reports_key=settings.PRZELEWY24_CONFIG["REPORTS_KEY"],  # type: ignore[arg-type]
            crc_key=settings.PRZELEWY24_CONFIG["CRC_KEY"],  # type: ignore[arg-type]
            notification_url=settings.PRZELEWY24_CONFIG["NOTIFICATION_URL"],  # type: ignore[arg-type]
            back_url=settings.PRZELEWY24_CONFIG["BACK_URL"],  # type: ignore[arg-type]
        ),
    )
    binder.bind_to_constructor(
        "payments_unit_of_work",
        payment_adapters.DjangoPaymentsUnitOfWork,
    )
    binder.bind_to_constructor(
        "planner_unit_of_work",
        planner_adapters.DjangoPlannerUnitOfWork,
    )
    binder.bind_to_constructor(
        "points_query_repository", todo_adapters.DjangoPointsQueryRepository
    )
    binder.bind_to_constructor(
        "sms_notificator",
        notification_adapters.DummySmsNotificator,
    )
    binder.bind("task_dispatcher", task_dispatchers.CeleryTaskDispatcher())
    binder.bind_to_constructor(
        "todos_query_repository", todo_adapters.DjangoTodosQueryRepository
    )
    binder.bind_to_constructor(
        "todos_unit_of_work", todo_adapters.DjangoTodosUnitOfWork
    )
    binder.bind_to_constructor(
        "users_query_repository", user_adapters.DjangoUsersQueryRepository
    )
    binder.bind_to_constructor(
        "users_unit_of_work", user_adapters.DjangoUsersUnitOfWork
    )

inject.configure(inject_config, once=True)
