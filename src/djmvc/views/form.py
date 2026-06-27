from django.contrib import messages
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

    def get_form_valid_message(self):
        return f'{self.title}: success'

    @property
    def form_valid_message(self):
        return self.get_form_valid_message()

    def get_form_invalid_message(self, form):
        labels = []
        for name in form.errors:
            if name == '__all__':
                continue
            field = form.fields.get(name)
            label = field.label if field and field.label else name
            labels.append(str(label))
        if not labels:
            return None
        return f'{self.title}: errors in {", ".join(labels)}'

    def message_success(self):
        messages.success(self.request, self.form_valid_message)

    def message_error(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, str(error))
        if msg := self.get_form_invalid_message(form):
            messages.error(self.request, msg)

    def form_valid(self, form):
        self.form = form
        self.message_success()
        return super().form_valid(form)

    def form_invalid(self, form):
        self.message_error(form)
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class FormView(FormMixin, TemplateViewMixin, generic.FormView):
    pass
