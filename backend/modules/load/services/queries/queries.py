from .dtos import DetailedOutputData, OutputData

#todo use these functions in view 
def get_data(
    repository: AbstractReservationsQueryRepository,
    reservation_id: ReservationId,
    participant_id: user_value_objects.USER_ID_TYPE | None = None,
) -> DetailedOutputData:
    return repository.get(reservation_id=reservation_id, participant_id=participant_id)


def list_data(
    repository: AbstractReservationsQueryRepository,
    filters: ReservationFilters | None = None,
    ordering: ReservationOrdering | None = None,
    pagination: Pagination | None = None,
) -> tuple[list[OutputData], int]:
    if filters is None:
        filters = ReservationFilters()

    if ordering is None:
        ordering = ReservationOrdering(
            timestamp=Ordering(order=OrderingOrder.DESCENDING, priority=1),
        )

    if pagination is None:
        pagination = Pagination(
            offset=PAGINATION_DEFAULT_OFFSET,
            records_per_page=PAGINATION_DEFAULT_LIMIT,
        )

    return repository.list(
        filters=filters,
        ordering=ordering,
        pagination=pagination,
    )
