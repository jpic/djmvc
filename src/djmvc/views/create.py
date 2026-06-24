from django.views import generic

from ..view import ViewMixin
from ..model import ModelMixin
from .form import FormMixin
from .template import TemplateMixin


class CreateView(ModelMixin, TemplateMixin, FormMixin, ViewMixin, generic.CreateView):
    tags = ['model']
    default_template_name = 'djmvc/form.html'
    icon = 'plus-circle'
    color = 'success'
