from modules.common import ordering as ordering_dtos


def get_django_ordering(ordering: dict[str, ordering_dtos.Ordering]) -> list[str]:
    return [
        (
            f"{field}"
            if order.order == ordering_dtos.OrderingOrder.ASCENDING
            else f"-{field}"
        )
        for field, order in sorted(
            ordering.items(), key=lambda order: order[1].priority
        )
    ]
