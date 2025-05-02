from modules.extract.domain import value_objects

from .... import fakers as common_fakers


def fake_extract_history() -> value_objects.ExtractHistory:
    return value_objects.ExtractHistory(
        input_file_name=common_fakers.fake_file_name(),
        saved_file_name=common_fakers.fake_file_name(),
        timestamp=common_fakers.fake_timestamp(),
    )
