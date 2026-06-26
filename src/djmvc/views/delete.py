import functools

from django.contrib.admin.utils import NestedObjects
from django.db import router
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.text import capfirst
from django.views import generic

from .form import FormView
from .list_action import ListActionMixin
from .template import TemplateViewMixin
from .objectform import ObjectFormMixin


def get_deleted_objects(view, objs):
    """
    Find objects related to ``objs`` that would be deleted (cascade).

    Return a tuple of ``(nested_objects, model_count, protected)``.
    """
    try:
        obj = objs[0]
    except (IndexError, TypeError):
        return [], {}, []

    if hasattr(objs, 'exists') and not objs.exists():
        return [], {}, []

    using = router.db_for_write(obj._meta.model)
    collector = NestedObjects(using=using, origin=objs)
    collector.collect(objs)

    def format_callback(obj):
        opts = obj._meta
        label = capfirst(opts.verbose_name)
        detail_urlname = getattr(view, 'detail_urlname', None)
        if obj._meta.model == view.model and detail_urlname:
            try:
                url = reverse(detail_urlname, args=[obj.pk])
            except NoReverseMatch:
                return f'{label}: {obj}'
            return format_html(
                '{}: <a href="{}" up-layer="new modal" up-size="large">{}</a>',
                label,
                url,
                obj,
            )
        return f'{label}: {obj}'

    to_delete = collector.nested(format_callback)
    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {
        capfirst(model._meta.verbose_name_plural): len(model_objs)
        for model, model_objs in collector.model_objs.items()
    }
    return to_delete, model_count, protected


class DeleteMixin:
    default_template_name = 'djmvc/form_delete.html'
    icon = 'trash'
    color = 'danger'

    @property
    def submit_button_label(self):
        return 'Delete'

    @functools.cached_property
    def detail_urlname(self):
        detail_route = self.controller.find_route('detail')
        if detail_route is None:
            return None
        return type(detail_route)(request=self.request).urlfullname

    @functools.cached_property
    def deletion_targets(self):
        if hasattr(self, 'object_list'):
            return self.object_list
        if getattr(self, 'object', None) is not None:
            return self.model._default_manager.filter(pk=self.object.pk)
        return self.model._default_manager.none()

    @functools.cached_property
    def _deletion_info(self):
        return get_deleted_objects(self, self.deletion_targets)

    @property
    def deleted_objects(self):
        return self._deletion_info[0]

    @property
    def deletion_summary(self):
        return self._deletion_info[1].items()

    @property
    def deletion_protected(self):
        return self._deletion_info[2]

    @property
    def has_deletion_cascade(self):
        model_count = self._deletion_info[1]
        if len(model_count) > 1:
            return True
        target_count = self.deletion_targets.count()
        return sum(model_count.values()) > target_count

    @property
    def can_confirm_delete(self):
        return not self.deletion_protected


class DeleteView(DeleteMixin, ObjectFormMixin, TemplateViewMixin, generic.DeleteView):
    tags = ['object']

    @property
    def message(self):
        return f'Are you sure you want to delete {self.object}?'

    def get_form_valid_message(self):
        return f'Deleted {self.object}'

    def form_valid(self, form):
        if not self.can_confirm_delete:
            return self.form_invalid(form)
        return super().form_valid(form)


class DeleteObjectsView(DeleteMixin, ListActionMixin, FormView):
    message = 'Are you sure you want to delete the selected items?'

    @property
    def title(self):
        return 'Delete'

    def get_form_valid_message(self):
        count = self._deleted_count
        if count == 1:
            label = capfirst(self.model._meta.verbose_name)
        else:
            label = capfirst(self.model._meta.verbose_name_plural)
        return f'Deleted {count} {label}'

    def form_valid(self, form):
        if not self.can_confirm_delete:
            return self.form_invalid(form)
        self._deleted_count = self.object_list.count()
        self.object_list.delete()
        return super().form_valid(form)