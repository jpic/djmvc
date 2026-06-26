from django.views import generic

from ..view import ViewMixin
from .modelform import ModelFormMixin
from .template import TemplateMixin


class CreateView(ModelFormMixin, TemplateMixin, ViewMixin, generic.CreateView):
    tags = ['model']
    default_template_name = 'djmvc/form.html'
    icon = 'plus-circle'
    color = 'success'
