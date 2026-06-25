from django.views import generic
from django.forms import Form
from djmvc.view import ViewMixin
from djmvc.views.template import TemplateMixin


class FormMixin:
    default_template_name = 'form.html'
    form_attributes = {
        'up-submit': True,
        'up-layer': 'any',
        'up-accept-location': '*',
        'up-on-accepted': 'up.visit(value.response.url)',
    }

    @property
    def submit_button_label(self):
        return self.title

    def get_form_class(self):
        return getattr(self, 'form_class', None) or Form

    def get_success_url(self):
        return self.request.POST.get('next', '/')


class FormView(ViewMixin, TemplateMixin, FormMixin, generic.FormView):
    pass
