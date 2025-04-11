from datetime import timedelta

from modules.extract.domain import value_objects
from . import fakers


class BatchMixin:
    @classmethod
    def create_batch(cls, size: int, **kwargs) -> list:
        if not isinstance(size, int) or size < 1:
            raise ValueError("Size must be a positive integer")

        return [cls.create(**kwargs) for _ in range(size)]  # type: ignore[attr-defined]


class ExtractHistoryFactory(BatchMixin):
    @staticmethod
    def create(**kwargs) -> value_objects.ExtractHistory:
        return value_objects.ExtractHistory(
            input_file_name=kwargs.get("input_file_name", fakers.fake_file_name()),
            saved_file_name=kwargs.get("saved_file_name", fakers.fake_file_name()),
            timestamp=kwargs.get("saved_file_name", fakers.fake_timestamp()),
        )
