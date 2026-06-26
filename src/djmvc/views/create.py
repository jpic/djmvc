from django.views import generic

from .modelform import ModelFormMixin
from .template import TemplateViewMixin


class CreateView(ModelFormMixin, TemplateViewMixin, generic.CreateView):
    tags = ['model']
    default_template_name = 'djmvc/form.html'
    icon = 'plus-circle'
    color = 'success'
