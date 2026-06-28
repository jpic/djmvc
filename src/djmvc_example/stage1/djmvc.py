import djmvc

from djmvc_example.stage0.models import Item


class ItemController(djmvc.ModelController):
    model = Item
    icon = 'inbox'


class InventoryController(djmvc.Controller):
    icon = 'boxes'
    routes = [
        ItemController,
    ]


djmvc.site.routes.append(InventoryController)