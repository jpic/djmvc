from django.utils.text import capfirst
from django.utils.translation import gettext as _
from django.views import generic

from .log import ADDITION
from .modelform import ModelFormMixin
from .template import TemplateViewMixin


class CreateView(ModelFormMixin, TemplateViewMixin, generic.CreateView):
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