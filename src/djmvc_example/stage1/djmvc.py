import djmvc
from django.utils.translation import gettext_lazy as _

from djmvc_example.stage0.models import Item


class ItemController(djmvc.ModelController):
    model = Item
    icon = 'boxes'
    routes = djmvc.ModelController.routes + [
        djmvc.generic.ListView.clone(title=_('Inventory')),
    ]


class InventoryController(djmvc.Controller):
    icon = 'boxes'
    routes = [
        ItemController,
    ]


djmvc.site.routes.append(InventoryController)