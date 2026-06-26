from django.urls import include, path

from .clonable import Clonable
from .registry import Registry
from .route import Route


class ControllerMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        routes = namespace.get('routes')
        if isinstance(routes, (list, tuple)):
            namespace['_declared_routes'] = namespace.pop('routes')
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class Controller(Clonable, Route, metaclass=ControllerMeta):
    @property
    def routes(self):
        if '_registry' not in self.__dict__:
            declared = None
            for cls in type(self).__mro__:
                if '_declared_routes' in cls.__dict__:
                    declared = cls.__dict__['_declared_routes']
                    break
            self.__dict__['_registry'] = Registry(self, declared or ())
        return self.__dict__['_registry']

    @property
    def codename(self):
        return super().codename.replace('controller', '')

    def find_route(self, codename):
        current = self
        while current is not None:
            try:
                return current.routes[codename]
            except KeyError:
                current = getattr(current, 'controller', None)
        return None

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