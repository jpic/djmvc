import djmvc

from .views import AutocompleteView


djmvc.ModelController.routes.append(AutocompleteView)