from django.urls import include, path

from .clonable import Clonable
from .route import Route


class Routes(list):
    def __init__(self, controller, routes):
        self.controller = controller

        for route in routes:
            route.controller = self.controller

        routes = [
            route() if isinstance(route, type) else route
            for route in routes
        ]

        super().__init__(routes)


class Controller(Clonable, Route):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(self.routes, Routes):
            self.routes = Routes(self, self.routes)

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
