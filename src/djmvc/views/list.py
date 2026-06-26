from django.views import generic
from ..model import ModelMixin
from .filter import FilterMixin
from .pagination import PaginationMixin
from .template import TemplateViewMixin
from .tables2 import Tables2Mixin


class ListMixin:
    default_template_name = 'djmvc/list.html'
    tags = ['navigation']
    urlpath = ''

    @property
    def title(self):
        return self.model._meta.verbose_name_plural.capitalize()

    def breadcrumbs(self):
        return []


class ListView(
    ListMixin,
    FilterMixin,
    PaginationMixin,
    Tables2Mixin,
    TemplateViewMixin,
    ModelMixin,
    generic.ListView,
):
    pagination_target = '[up-list]'
    filter_target = '[up-list]'
