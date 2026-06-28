from django.utils.module_loading import autodiscover_modules

from .controller import Controller
from .view import View
from .model import ModelMixin
from .views import generic



class ModelController(ModelMixin, Controller):
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
        return self.model.__name__.lower()

    def has_permission(self, view):
        return view.has_permission_backend()

    def get_queryset(self, view):
        return self.model._default_manager.all()


class Home(generic.TemplateView):
    urlpath = ''

    def has_permission(self):
        return True


class Site(Controller):
    urlpath = ''
    routes = [
        Home,
    ]

    def autodiscover(self):
        autodiscover_modules('djmvc')
        return self

    def build(self):
        self.autodiscover()
        return super().build()


site = Site()