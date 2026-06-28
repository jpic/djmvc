from django.utils.text import capfirst
from django.utils.translation import gettext as _
from django.views import generic

from .template import TemplateViewMixin
from .objectform import ObjectModelFormMixin


class UpdateView(ObjectModelFormMixin, TemplateViewMixin, generic.UpdateView):
    tags = ['object']
    default_template_name = 'form.html'
    icon = 'pencil'
    color = 'warning'

    @property
    def title(self):
        return _('Change %(name)s') % {
            'name': capfirst(self.model._meta.verbose_name),
        }