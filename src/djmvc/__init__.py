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
        generic.CreateView,
    ]

    @property
    def codename(self):
        return self.model.__name__.lower()


class Home(generic.TemplateView):
    urlpath = ''


class Site(Controller):
    urlpath = ''
    routes = [
        Home,
    ]

    def autodiscover(self):
        autodiscover_modules('djmvc')
        return self


site = Site()
