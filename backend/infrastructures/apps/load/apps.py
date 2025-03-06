from django.apps import AppConfig

from ..common.apps import InjectAppConfigMixin


class LoadConfig(InjectAppConfigMixin, AppConfig):
    name = "infrastructures.apps.load"
