from django.apps import AppConfig


class HrmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hrm_app'

    def ready(self):
        # Importieren Sie Ihre Signale hier
        from . import signals