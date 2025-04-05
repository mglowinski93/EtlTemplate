import os
from datetime import datetime
from dateutil import tz

TIME_ZONE = os.environ["TZ"]


def get_currect_timestamp() -> datetime:
    return datetime.now(tz=tz.gettz(TIME_ZONE))
