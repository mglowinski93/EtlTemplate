def map_bool_query_parameter_to_bool(value: str | None) -> bool | None:
    if value is None:
        return None

    _value = value.strip().lower()
    if _value in {"true", "1", "yes"}:
        return True
    if _value in {"false", "0", "no"}:
        return False

    raise ValueError
