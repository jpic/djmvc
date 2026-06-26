import djmvc

from .views import Stage0Controller

djmvc.site.routes.append(Stage0Controller)