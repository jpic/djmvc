import functools

from django.views import generic
from ..model import ModelMixin
from .filter import FilterMixin
from .object import ObjectMixin
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

    @functools.cached_property
    def list_actions(self):
        return self.controller.get_tagged_views('list_action', request=self.request)


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


class DetailListView(ObjectMixin, ListView):
    default_template_name = 'djmvc/detaillist.html'
    tags = ['object']

    @property
    def title(self):
        return super(ListMixin, self).title
