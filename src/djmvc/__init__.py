"""djmvc public API.

:data:`site` is the root :class:`Site` controller. Append controllers to
``site.routes`` in each app's ``djmvc.py`` module; :meth:`Site.build` imports
those modules via autodiscovery (like Django admin's ``admin.py``).
"""

from django.utils.module_loading import autodiscover_modules

from .controller import Controller
from .view import View
from .model import ModelMixin
from .views import generic


class ModelController(ModelMixin, Controller):
    """CRUD controller for a single Django model.

    Attributes:
        routes: Default list, detail, create, update, delete, and bulk-delete
            views. Extend with ``ModelController.routes + [MyView]`` or
            replace entries by codename (see :class:`~djmvc.registry.Registry`).
        model: Django model class managed by this controller.
        icon (str): Bootstrap Icons name for the navigation list view.
        color (str): Bulma color for the navigation list icon.
    """

    routes = [
        generic.ListView,
        generic.DetailView,
        generic.UpdateView,
        generic.DeleteView,
        generic.DeleteObjectsView,
        generic.CreateView,
    ]

    @property
    def codename(self):
        """URL segment from :attr:`model` name (lowercase)."""
        return self.model.__name__.lower()

    def has_permission(self, view):
        """Check Django permissions for *view* via the permission backend."""
        return view.has_permission_backend()

    def get_queryset(self, view):
        """Return all rows for *view*; override to scope per user or role."""
        return self.model._default_manager.all()


class Home(generic.TemplateView):
    """Site root page at ``/``."""

    urlpath = ''

    def has_permission(self):
        """Allow anonymous access to the home page."""
        return True


class Site(Controller):
    """Root site controller; autodiscovers ``djmvc.py`` in installed apps."""

    urlpath = ''
    routes = [
        Home,
    ]

    def autodiscover(self):
        """Import ``djmvc`` modules from every installed app."""
        autodiscover_modules('djmvc')
        return self

    def build(self):
        """Autodiscover app routes, then build the route registry."""
        self.autodiscover()
        return super().build()


site = Site()