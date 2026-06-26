from django.views import generic
from django.forms import Form
from djmvc.views.template import TemplateViewMixin


class FormMixin:
    default_template_name = 'form.html'
    form_attributes = {
        'up-submit': True,
        'up-layer': 'any',
        'up-accept-location': '*',
        'up-on-accepted': 'up.visit(response.url)',
    }

    @property
    def submit_button_label(self):
        return self.title

    def unpoly_attributes(self, context=None):
        attrs = {
            'up-layer': 'new modal',
            'up-size': 'medium',
        }
        if request := getattr(self, 'request', None):
            attrs['up-accept-location'] = request.path
        return attrs

    def get_form_class(self):
        return getattr(self, 'form_class', None) or Form

    def get_success_url(self):
        return self.request.POST.get('next', '/')


class FormView(TemplateViewMixin, FormMixin, generic.FormView):
    pass
