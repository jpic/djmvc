from django.urls import include, path

from .clonable import Clonable
from .registry import Registry
from .route import Route


class RoutesDescriptor:
    """Return the built registry on instances after build(), else the declaration list."""

    def __get__(self, instance, owner):
        obj = instance or owner
        return getattr(obj, 'registry', obj._declaration)


class ControllerMeta(type):
    """Move class-body ``routes = [...]`` into ``_declaration``; wire ``routes`` as the accessor."""

    def __new__(mcs, name, bases, namespace):
        routes = namespace.pop('routes', None)
        cls = super().__new__(mcs, name, bases, namespace)
        if routes is None:
            cls._declaration = list(bases[0]._declaration) if bases else []
        else:
            cls._declaration = list(routes)
        cls.routes = RoutesDescriptor()
        return cls


class Controller(Clonable, Route, metaclass=ControllerMeta):
    routes = []

    def build(self):
        self.registry = Registry(self, list(type(self)._declaration))
        for route in self.routes:
            if build := getattr(route, 'build', None):
                build()
        return self

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

    @property
    def model_controller(self):
        # FIXME: candidate for redesign — walk to the nearest ancestor ModelController
        current = self
        while current is not None:
            if getattr(type(current), 'model', None) is not None:
                return current
            current = getattr(current, 'controller', None)
        return self

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