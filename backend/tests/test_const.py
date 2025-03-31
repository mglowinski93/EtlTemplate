import pathlib


#TODO use it to refer to resource csv etc.
SQL_INJECTION_STRING = "SQL ' injection; DROP SCHEMA public CASCADE;"

EXAMPLE_VIDEO_PATH = (
    pathlib.Path(__file__).parent / "test_files" / "courses" / "example_video.mp4"
)
EXAMPLE_THUMBNAIL_PATH = (
    pathlib.Path(__file__).parent / "test_files" / "courses" / "example_thumbnail.png"
)
