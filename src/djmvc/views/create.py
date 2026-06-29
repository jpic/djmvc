from django.utils.text import capfirst
from django.utils.translation import gettext as _
from django.views import generic

from .json import JsonFormMixin, json_method_not_allowed
from .log import ADDITION
from .modelform import ModelFormMixin
from .swagger import swagger_write_operation
from .template import TemplateViewMixin


class CreateView(
    JsonFormMixin,
    ModelFormMixin,
    TemplateViewMixin,
    generic.CreateView,
):
    """Create a new model instance.

    Attributes:
        permission_shortcode (str): Default ``'add'``.
        tags (list[str]): Default ``['model']`` (top-bar create button).
        default_template_name (str): Form template.
        icon (str): Bootstrap Icons name.
        color (str): Bulma button colour modifier.
        fields (list[str]): Model form fields. Set on clone or subclass.
        form_class (type): Explicit form class instead of ``fields``.
    """

    permission_shortcode = 'add'
    tags = ['model']
    default_template_name = 'djmvc/form.html'
    icon = 'plus-circle'
    color = 'success'
    log_action_flag = ADDITION

    @property
    def title(self):
        return _('Add %(name)s') % {
            'name': capfirst(self.model._meta.verbose_name),
        }

    json_method_names = ('post',)

    def json_get(self, request, *args, **kwargs):
        return json_method_not_allowed(self.json_method_names)

    def get_swagger_post(self):
        return swagger_write_operation(self, str(self.title))