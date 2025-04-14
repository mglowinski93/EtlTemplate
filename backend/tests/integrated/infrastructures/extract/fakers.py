from modules.extract.domain import value_objects

from .... import fakers


def fake_extract_history() -> value_objects.ExtractHistory:
    return value_objects.ExtractHistory(
        input_file_name=fakers.fake_file_name(10),
        saved_file_name=fakers.fake_file_name(),
        timestamp=fakers.fake_timestamp(),
    )
