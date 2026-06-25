import djmvc
from django.apps import AppConfig


class DjmvcAuthConfig(AppConfig):
    name = "djmvc_auth"

    def ready(self):
        from .views import AuthController
        djmvc.site.routes.register(AuthController)
