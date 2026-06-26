from django.views import generic

from .template import TemplateViewMixin
from .objectform import ObjectModelFormMixin


class UpdateView(ObjectModelFormMixin, TemplateViewMixin, generic.UpdateView):
    tags = ['object']
    default_template_name = 'form.html'
    icon = 'pencil'
    color = 'warning'
