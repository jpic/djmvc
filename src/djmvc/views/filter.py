import functools
import operator
from functools import reduce

from crispy_forms.helper import FormHelper
from django import forms
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _


class FilterMixin:
    """Search and field filters on list querysets.

    Attributes:
        search_param (str): GET parameter for full-text search. Default
            ``'search'``.
        filter_fields (list[str] | None): Model field names rendered as filter
            inputs. ``None`` uses search only.
        filter_form_class (type | None): Custom filter form class. When unset, a
            form is built from ``filter_fields``.
        filter_target (str): Unpoly ``up-target`` for the filter form.
    """

    search_param = 'search'
    filter_fields = None
    filter_form_class = None
    filter_target = '[up-list]'

    @property
    def filter_submit_label(self):
        """Label for the filter form submit button."""
        return _('Apply')

    @functools.cached_property
    def search_fields(self):
        """CharField and TextField names searched by :attr:`search_param`."""
        return [
            f.name
            for f in self.model_meta.get_fields()
            if f.concrete
            and not f.is_relation
            and isinstance(f, (models.CharField, models.TextField))
        ]

    def get_filter_field_names(self):
        """Filter form field names including :attr:`search_param` when applicable."""
        names = list(self.filter_fields or [])
        if self.search_fields and self.search_param not in names:
            names.insert(0, self.search_param)
        return names

    def filter_field_for(self, name):
        if name == self.search_param:
            return forms.CharField(label='', required=False)
        return self.model_meta.get_field(name).formfield()

    def get_filter_form_class(self):
        """Return :attr:`filter_form_class` or build one from :attr:`filter_fields`."""
        if (
            'filter_form_class' in type(self).__dict__
            and type(self).filter_form_class is not None
        ):
            return type(self).filter_form_class
        return self._build_default_filter_form_class()

    def _uses_default_filter_form(self):
        return 'filter_form_class' not in type(self).__dict__

    def _build_default_filter_form_class(self):
        field_names = self.get_filter_field_names()
        if not field_names:
            return None

        view = self
        form_fields = {
            name: self.filter_field_for(name)
            for name in field_names
        }

        def __init__(form_self, *args, view=None, **kwargs):
            forms.Form.__init__(form_self, *args, **kwargs)
            form_self.helper = FormHelper()
            form_self.helper.form_method = 'get'
            form_self.helper.form_tag = False
            form_self.helper.disable_csrf = True
            form_self.helper.form_show_labels = False
            if view is not None:
                page_kwarg = getattr(view, 'page_kwarg', 'page')
                for key, value in view.request.GET.items():
                    if key in form_self.fields or key == page_kwarg:
                        continue
                    form_self.fields[key] = forms.CharField(
                        widget=forms.HiddenInput(),
                        initial=value,
                    )

        form_fields['__init__'] = __init__
        return type(
            f'{self.model.__name__}FilterForm',
            (forms.Form,),
            form_fields,
        )

    @functools.cached_property
    def filter_form(self):
        """Bound filter form from the current GET parameters."""
        form_class = self.get_filter_form_class()
        if form_class is None:
            return None
        if self._uses_default_filter_form():
            return form_class(self.request.GET, view=self)
        return form_class(self.request.GET)

    @property
    def filter_attributes(self):
        """HTML attributes for the filter ``<form>`` tag."""
        return {
            'up-submit': True,
            'up-target': self.filter_target,
            'up-history': True,
        }

    @property
    def has_active_filters(self):
        """Whether any visible filter field has a value."""
        form = self.filter_form
        if form is None:
            return False
        return any(
            form.data.get(name)
            for name, field in form.fields.items()
            if not isinstance(field.widget, forms.HiddenInput)
        )

    def clear_filter_url(self):
        """URL with filter and page GET parameters removed."""
        qs = self.request.GET.copy()
        form = self.filter_form
        if form is not None:
            for name, field in form.fields.items():
                if not isinstance(field.widget, forms.HiddenInput):
                    qs.pop(name, None)
        page_kwarg = getattr(self, 'page_kwarg', 'page')
        qs.pop(page_kwarg, None)
        path = self.request.path
        return f'{path}?{qs.urlencode()}' if qs else path

    def get_queryset(self):
        """Apply search-term filtering to the scoped queryset."""
        qs = super().get_queryset()
        form = self.filter_form
        if form is None:
            return qs
        if not form.is_valid():
            return qs
        term = form.cleaned_data.get(self.search_param, '')
        if not term or not self.search_fields:
            return qs
        return qs.filter(
            reduce(
                operator.or_,
                [
                    Q(**{f'{field}__icontains': term})
                    for field in self.search_fields
                ],
            )
        ).distinct()