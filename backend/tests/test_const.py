import pathlib


EXTRACT_TEST_FILES_LOCATION = pathlib.Path(__file__).parent / "test_files" / "extract"
CORRECT_INPUT_CSV = (
    pathlib.Path(__file__).parent / "test_files" / "extract" / "correct_input.csv"
)
DATASET_INPUT_SIZE = (
    10
)
CORRECT_INPUT_XLS = (
    pathlib.Path(__file__).parent / "test_files" / "extract" / "correct_input.xls"
)
CORRECT_INPUT_XLSX = (
    pathlib.Path(__file__).parent / "test_files" / "extract" / "correct_input.xlsx"
)
INCORRECT_INPUT = (
    pathlib.Path(__file__).parent
    / "test_files"
    / "extract"
    / "incorrect_data_input.csv"
)
NOT_SUPPORTED_INPUT = (
    pathlib.Path(__file__).parent
    / "test_files"
    / "extract"
    / "not_supported_extension.png"
)
TRANSFORM_CORRECT_INPUT_CSV = (
    pathlib.Path(__file__).parent / "test_files" / "transform" / "correct_input.csv"
)
