import logging
import os


logging.basicConfig(
    level=logging.getLevelName(os.environ["LOG_LEVEL"]),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
