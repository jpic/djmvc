from django.urls import include, path

from .clonable import Clonable
from .route import Route


class Routes(list):
    def __init__(self, controller, routes=None):
        self.controller = controller
        super().__init__()
        for route in routes or []:
            self.append(route)

    def __getitem__(self, codename_or_index):
        try:
            return super().__getitem__(codename_or_index)
        except TypeError:
            for route in self:
                if route.codename == codename_or_index:
                    return route
            raise KeyError(codename_or_index)

    def append(self, route):
        if isinstance(route, type):
            route = route()
        route.controller = self.controller
        super().append(route)


class Controller(Clonable, Route):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.routes = Routes(self, getattr(self, 'routes', None))

    @property
    def codename(self):
        return super().codename.replace('controller', '')

    def get_tagged_views(self, tag, **kwargs):
        def process(controller):
            views = []
            for route in controller.routes:
                if isinstance(route, Controller):
                    views += process(route)
                    continue

                if tag not in getattr(route, 'tags', []):
                    continue

                view = type(route)(**kwargs)
                if view.has_permission():
                    views.append(view)
            return views
        return process(self)

    @property
    def root(self):
        controller = getattr(self, 'controller', None)
        if not controller:
            return self

        while hasattr(controller, 'controller'):
            controller = controller.controller
        return controller

    @property
    def urlpatterns(self):
        patterns = []

        for route in self.routes:
            patterns += route.urlpatterns

        return [
            path(
                self.urlpath,
                include(
                    (patterns, self.urlname),
                    namespace=self.urlname,
                ),
            )
        ]
