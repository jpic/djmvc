import djmvc

from .models import Item


class ItemController(djmvc.ModelController):
    model = Item


djmvc.site.routes.append(ItemController)