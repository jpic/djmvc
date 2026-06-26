import djmvc

from .views import Stage0Controller

djmvc.site.routes.register(Stage0Controller)