from modules.extract.domain import value_objects
from modules.transform.domain import value_objects as transform_value_objects

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


class TransformedDataFactory(BatchMixin):
    @staticmethod
    def create(**kwargs) -> list[transform_value_objects.TransformedData]:
        return [
            transform_value_objects.TransformedData(
                full_name=kwargs.get("full_name", fakers.fake_name()),
                age=kwargs.get("age", fakers.fake_age()),
                is_satisfied=kwargs.get("is_satisfied", fakers.fake_is_satisfied()),
            )
        ]
