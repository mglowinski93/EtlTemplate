# pylint: disable=wildcard-import,unused-wildcard-import

from .django_settings import *  # noqa: F403
from .auth_settings import *  # noqa: F403
from .app_settings import *  # noqa: F403


DEBUG = False

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",  # nosec B108
    }
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
] + MIDDLEWARE  # noqa: F405

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static", "dist")  # noqa: F405
