from .app_settings import *  # noqa: F403
from .auth_settings import *  # noqa: F403
from .django_settings import *  # noqa: F403
from .logging_settings import *  # noqa: F403

try:
    from .local_settings import *  # type: ignore[import-not-found] # noqa: F403
except ImportError:
    pass
