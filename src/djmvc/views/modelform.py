from django.forms import modelform_factory

from ..model import ModelMixin
from .form import FormMixin


class ModelFormMixin(ModelMixin, FormMixin):
    fields = '__all__'

    def get_form_valid_message(self):
        return f'{self.title}: {self.form.instance}'

    def get_form_class(self):
        if getattr(self, 'form_class', None):
            return self.form_class
        return modelform_factory(self.model, fields=self.fields)
