import djmvc

from .models import Item


class ItemController(djmvc.ModelController):
    model = Item
    icon = 'inbox'
    routes = djmvc.ModelController.routes + [
        djmvc.generic.ListView.clone(site_search=True),
    ]


djmvc.site.routes.append(ItemController)