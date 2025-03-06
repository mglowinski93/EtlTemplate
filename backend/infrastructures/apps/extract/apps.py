from django.apps import AppConfig

from ..common.apps import InjectAppConfigMixin


class ExtractConfig(InjectAppConfigMixin, AppConfig):
    name = "infrastructures.apps.extract"
