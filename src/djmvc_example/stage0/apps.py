import djmvc
from django.apps import AppConfig


class Stage0Config(AppConfig):
    name = "djmvc_example.stage0"

    def ready(self):
        from .views import Stage0Controller
        djmvc.site.routes.register(Stage0Controller)
