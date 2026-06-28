from django.core.exceptions import ImproperlyConfigured

from .controller import Controller


class ModelMixin:
    """
    Allows setting model on the class, or uses the controller model if any.
    """
    @property
    def title(self):
        return super().title.replace(self.model.__name__, '')

    @property
    def codename(self):
        return super().codename.replace(self.model.__name__.lower(), '')

    @property
    def model(self):
        """ Return self.controller.model """
        current = self.controller
        while not hasattr(current, 'model'):
            try:
                current = current.controller
            except AttributeError:
                raise Exception('Model not found')
        return current.model

    @property
    def model_meta(self):
        # because django template won't allow ._meta because it starts with an
        # underscore ...
        return self.model._meta

    def _controller_queryset(self):
        if self.controller:
            mc = getattr(self.controller, 'model_controller', self.controller)
            if hasattr(mc, 'get_queryset'):
                return mc.get_queryset(self)
        if self.model:
            return self.model._default_manager.all()
        raise ImproperlyConfigured(
            '%(cls)s is missing a QuerySet. Define %(cls)s.model, '
            '%(cls)s.queryset, or override %(cls)s.get_queryset().' % {
                'cls': self.__class__.__name__,
            }
        )

    def get_object_queryset(self):
        """Scoped model rows for resolving ``self.object`` from the URL."""
        return self._controller_queryset()

    def get_queryset(self):
        return self._controller_queryset()

    def breadcrumbs(self, with_self=True):
        crumbs = []
        list_route = self.controller.find_route('list')
        if list_route:
            list_view = type(list_route)(request=self.request)
            if list_view.has_permission():
                crumbs.append(list_view)
        if with_self:
            crumbs.append(self)
        return crumbs
