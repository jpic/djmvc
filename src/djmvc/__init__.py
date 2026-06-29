"""djmvc public API.

:data:`site` is the root :class:`Site` controller. Append controllers to
``site.routes`` in each app's ``djmvc.py`` module; :meth:`Site.build` imports
those modules via autodiscovery (like Django admin's ``admin.py``).
"""

from django.db import models as db_models
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

    json_fields = None

    def get_json_fields(self):
        """Field names exposed in JSON responses."""
        if self.json_fields is not None:
            return list(self.json_fields)
        return [f.name for f in self.model._meta.fields]

    def get_FIELD_json(self, obj, field):
        value = getattr(obj, field)
        if callable(value):
            value = value()
        if value is not None and not isinstance(value, (str, int, float, bool)):
            value = str(value)
        return value

    def serialize(self, obj, fields=None):
        """Map a model instance to a JSON-serializable dict."""
        fields = fields or self.get_json_fields()
        return {
            field: getattr(
                self,
                f'get_{field}_json',
                self.get_FIELD_json,
            )(obj, field)
            for field in fields
        }

    def get_swagger_model_name(self, request):
        return self.model.__name__

    def get_swagger_model_definition(self, request):
        result = {'properties': {}, 'type': 'object'}
        int_fields = (
            db_models.IntegerField,
            db_models.BigIntegerField,
            db_models.AutoField,
            db_models.PositiveIntegerField,
            db_models.PositiveSmallIntegerField,
            db_models.SmallIntegerField,
        )
        for field in self.model._meta.fields:
            custom = getattr(self, f'swagger_field_{field.name}_definition', None)
            if custom:
                result['properties'][field.name] = custom
                continue
            field_def = {}
            if isinstance(field, int_fields):
                field_def['type'] = 'integer'
            elif isinstance(field, db_models.BooleanField):
                field_def['type'] = 'boolean'
            elif isinstance(field, db_models.JSONField):
                field_def['type'] = 'object'
            else:
                field_def['type'] = 'string'
            result['properties'][field.name] = field_def
        return result


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
