import functools

from django.utils.translation import gettext as _, ngettext
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

    @property
    def empty_list_message(self):
        return _('No %(verbose_name)s found matching the query') % {
            'verbose_name': self.model_meta.verbose_name_plural,
        }

    @property
    def list_action_count_label_one(self):
        return ngettext(
            '%(total_count)s selected',
            'All %(total_count)s selected',
            1,
        ) % {'total_count': 1}

    @property
    def list_action_count_label_other(self):
        return ngettext(
            '%(total_count)s selected',
            'All %(total_count)s selected',
            2,
        ) % {'total_count': '__COUNT__'}

    @property
    def filter_submit_label(self):
        return _('Apply')


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
