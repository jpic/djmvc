from django.views import generic
from ..view import ViewMixin
from ..model import ModelMixin
from .template import TemplateMixin
from .tables2 import Tables2Mixin


class ListMixin:
    default_template_name = 'djmvc/list.html'
    tags = ['navigation']
    urlpath = ''

    @property
    def name(self):
        return self.model._meta.verbose_name_plural.capitalize()


class ListView(ListMixin, Tables2Mixin, TemplateMixin, ModelMixin, ViewMixin, generic.ListView):
    pass
