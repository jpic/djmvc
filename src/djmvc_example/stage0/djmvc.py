import djmvc

from .models import Item


class ItemController(djmvc.ModelController):
    model = Item
    icon = 'inbox'


djmvc.site.routes.append(ItemController)