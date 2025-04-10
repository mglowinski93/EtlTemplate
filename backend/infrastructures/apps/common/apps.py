import inject


class InjectAppConfigMixin:
    def ready(self):
        from ...config.settings import injections_configurations

        inject.configure(injections_configurations.inject_config, once=True)
