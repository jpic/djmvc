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

site = Site()
