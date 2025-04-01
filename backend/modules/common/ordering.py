from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OrderingOrder(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


@dataclass(frozen=True)
class Ordering:
    order: OrderingOrder
    priority: int

    @staticmethod
    def create_ordering(data: list[str]) -> dict[str, Ordering]:
        ordering = {}
        for index, order in enumerate(data):
            field = order.strip()
            ordering_order = OrderingOrder.ASCENDING

            if order.startswith("-"):
                field = order[1:]
                ordering_order = OrderingOrder.DESCENDING
            ordering[field] = Ordering(order=ordering_order, priority=index + 1)

        return ordering
