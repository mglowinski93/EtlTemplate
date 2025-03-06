import inject


class InjectAppConfigMixin:
    def ready(self):
        from ...config.settings import injections_configuration

        inject.configure(injections_configuration.inject_config, once=True)
