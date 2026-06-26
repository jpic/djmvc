from django.views import generic

from .template import TemplateViewMixin
from .objectform import ObjectFormMixin


class DeleteView(ObjectFormMixin, TemplateViewMixin, generic.DeleteView):
    tags = ['object']
    template_name = 'djmvc/form.html'
    form_message = 'Are you sure you want to delete {{ view.object }} ?'
    icon = 'trash'
    color = 'danger'
