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
