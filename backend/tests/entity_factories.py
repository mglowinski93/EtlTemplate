class BatchMixin:
    @classmethod
    def create_batch(cls, size: int, **kwargs) -> list:
        if not isinstance(size, int) or size < 1:
            raise ValueError("Size must be a positive integer.")

        return [cls.create(**kwargs) for _ in range(size)]  # type: ignore[attr-defined]
