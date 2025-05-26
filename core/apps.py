from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # импортируем сигналы в методе ready
    def ready(self):
        import core.signals