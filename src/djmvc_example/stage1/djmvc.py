import djmvc

from djmvc_example.stage0.models import Item


class ItemController(djmvc.ModelController):
    model = Item


class InventoryController(djmvc.Controller):
    routes = [
        ItemController,
    ]


djmvc.site.routes.append(InventoryController)