import djmvc
from djmvc.views import generic

from .models import Controller, URL
from .routing_debug import DebugListMixin


class ControllerListView(DebugListMixin, generic.ListView):
    search_fields = ('app', 'model', 'codename')
    table_fields = ('app', 'model', 'codename', 'urlpath')


class URLListView(DebugListMixin, generic.ListView):
    search_fields = (
        'urlfullname',
        'fullurlpath',
        'view_class',
        'controller__app',
    )
    table_fields = ('controller', 'view_class', 'fullurlpath', 'urlfullname')


class RoutingDebugController(djmvc.Controller):
    codename = 'debug'
    icon = 'bug'
    color = 'warning'
    routes = [
        djmvc.ModelController.clone(
            model=Controller,
            icon='diagram-3',
            routes=[
                ControllerListView,
                generic.DetailView,
            ],
        ),
        djmvc.ModelController.clone(
            model=URL,
            icon='signpost-split',
            routes=[
                URLListView,
                generic.DetailView,
            ],
        ),
    ]