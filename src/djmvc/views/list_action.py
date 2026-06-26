import functools

from django.forms import Form

from ..model import ModelMixin
from .form import FormMixin, FormView


class ListActionMixin(ModelMixin, FormMixin):
    tags = ['list_action']

    def get_queryset(self):
        if queryset := getattr(self, 'queryset', None):
            return queryset
        return self.model._default_manager.all()

    @functools.cached_property
    def pks(self):
        return self.request.GET.getlist('pks') or self.request.POST.getlist('pks')

    @functools.cached_property
    def object_list(self):
        return self.get_queryset().filter(pk__in=self.pks)

    @functools.cached_property
    def invalid_pks(self):
        return len(self.pks) - self.object_list.count()

    def get_success_url(self):
        list_route = self.controller.find_route('list')
        return type(list_route)(request=self.request).url

    def get_form_class(self):
        return getattr(self, 'form_class', None) or Form

    @property
    def form_attributes(self):
        attrs = dict(FormMixin.form_attributes)
        attrs['up-on-finished'] = 'djmvcClearListActionSelections()'
        return attrs

    def unpoly_attributes(self, context=''):
        attrs = super().unpoly_attributes(context)
        if context == 'list_action_bar':
            attrs['data-list-action'] = 'urlupdate'
            attrs['up-on-accepted'] = (
                'djmvcClearListActionSelections(); up.visit(response.url)'
            )
        return attrs


class ListActionView(ListActionMixin, FormView):
    pass