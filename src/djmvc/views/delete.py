from django.views import generic

from ..view import ViewMixin
from ..model import ModelMixin
from .template import TemplateMixin
from .form import FormMixin


class DeleteView(FormMixin, ModelMixin, ViewMixin, generic.DeleteView):
    tags = ['object']
    template_name = 'djmvc/form.html'
    form_message = 'Are you sure you want to delete {{ view.object }} ?'
    urlpath = '<int:pk>/delete/'
    icon = 'trash'
    color = 'danger'
