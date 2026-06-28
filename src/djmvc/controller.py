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
    """Group child routes under a shared URL prefix.

    Attributes:
        routes: Declared child routes (classes or instances). Before
            :meth:`build`, this is the declaration list; afterward it is a
            :class:`~djmvc.registry.Registry` of built route instances.
        icon (str): Bootstrap Icons name for the sidebar entry. Navigation
            list views inherit this when they do not set their own ``icon``.
        color (str): Bulma color name for the sidebar icon (``primary``,
            ``info``, …).
    """

    routes = []

    def build(self):
        """Instantiate child routes into a :class:`~djmvc.registry.Registry`."""
        self.registry = Registry(self, list(type(self)._declaration))
        for route in self.routes:
            if build := getattr(route, 'build', None):
                build()
        return self

    @property
    def codename(self):
        """URL segment with the ``controller`` suffix removed from the class name."""
        return super().codename.replace('controller', '')

    def find_route(self, codename):
        """Walk up the controller tree and return the first route named *codename*."""
        current = self
        while current is not None:
            try:
                return current.routes[codename]
            except KeyError:
                current = getattr(current, 'controller', None)
        return None

    @property
    def model_controller(self):
        """Nearest ancestor :class:`~djmvc.ModelController`, or ``self``."""
        current = self
        while current is not None:
            if getattr(type(current), 'model', None) is not None:
                return current
            current = getattr(current, 'controller', None)
        return self

    def has_permission(self, view):
        """Delegate permission checks to the nearest :class:`~djmvc.ModelController`."""
        mc = self.model_controller
        if mc is not self:
            return mc.has_permission(view)
        return view.has_permission_backend()

    def get_tagged_views(self, tag, **kwargs):
        """Return permitted child views whose ``tags`` contain *tag*."""
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
        """Topmost controller ancestor."""
        controller = getattr(self, 'controller', None)
        if not controller:
            return self

        while hasattr(controller, 'controller'):
            controller = controller.controller
        return controller

    @property
    def urlpatterns(self):
        """Include child :attr:`~djmvc.route.Route.urlpatterns` under this prefix."""
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