from django.views import generic

from ..view import ViewMixin
from ..model import ModelMixin
from .template import TemplateMixin
from .modelform import ModelFormMixin


class UpdateView(ModelFormMixin, TemplateMixin, ViewMixin, generic.UpdateView):
    tags = ['object']
    default_template_name = 'form.html'
    urlpath = '<int:pk>/edit/'
    icon = 'pencil'
    color = 'warning'
