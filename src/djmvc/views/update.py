from django.utils.text import capfirst
from django.utils.translation import gettext as _
from django.views import generic

from .action import ActionMixin
from .json import JsonFormMixin, json_method_not_allowed
from .swagger import swagger_write_operation
from .template import TemplateViewMixin
from .objectform import ObjectModelFormMixin


class UpdateView(
    ActionMixin,
    JsonFormMixin,
    ObjectModelFormMixin,
    TemplateViewMixin,
    generic.UpdateView,
):
    """Update an existing model instance.

    Attributes:
        permission_shortcode (str): Default ``'change'``.
        tags (list[str]): Default ``['object']`` (object action menu).
        default_template_name (str): Form template.
        icon (str): Bootstrap Icons name.
        color (str): Bulma button colour modifier.
        fields (list[str]): Model form fields. Set on clone or subclass.
        form_class (type): Explicit form class instead of ``fields``.
    """

    permission_shortcode = 'change'
    tags = ['object']
    default_template_name = 'form.html'
    icon = 'pencil'
    color = 'warning'
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']
    json_method_names = ('put', 'patch')

    @property
    def title(self):
        return _('Change %(name)s') % {
            'name': capfirst(self.model._meta.verbose_name),
        }

    def json_post(self, request, *args, **kwargs):
        return json_method_not_allowed(self.json_method_names)

    def get_swagger_put(self):
        return swagger_write_operation(self, str(self.title))

    def get_swagger_patch(self):
        operation = swagger_write_operation(self, str(self.title))
        operation['summary'] = f'Partial update: {self.title}'
        return operation