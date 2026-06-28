from django.utils.text import capfirst
from django.utils.translation import gettext as _
from django.views import generic

from .action import ActionMixin
from .template import TemplateViewMixin
from .objectform import ObjectModelFormMixin


class UpdateView(
    ActionMixin,
    ObjectModelFormMixin,
    TemplateViewMixin,
    generic.UpdateView,
):
    permission_shortcode = 'change'
    tags = ['object']
    default_template_name = 'form.html'
    icon = 'pencil'
    color = 'warning'

    @property
    def title(self):
        return _('Change %(name)s') % {
            'name': capfirst(self.model._meta.verbose_name),
        }