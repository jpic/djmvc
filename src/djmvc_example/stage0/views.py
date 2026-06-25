import djmvc
from .models import Stage0Model


class Stage0Controller(djmvc.ModelController):
    model = Stage0Model
