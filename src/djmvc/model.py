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
