from django.apps import AppConfig


class DjmvcApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djmvc_api'
    verbose_name = 'djmvc API'

    def ready(self):
        import djmvc_api.models  # noqa: F401