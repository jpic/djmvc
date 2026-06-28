import djmvc

from .models import Stage0


class Stage0Controller(djmvc.ModelController):
    model = Stage0


djmvc.site.routes.append(Stage0Controller)