import djmvc
from django.apps import AppConfig
from django.conf import settings
from django.urls import reverse


class DjmvcAuthConfig(AppConfig):
    name = "djmvc_auth"

    def ready(self):
        from .views import AuthController

        djmvc.site.routes.register(AuthController)

        settings.LOGIN_URL = reverse('site:auth:login')
