from ..model import ModelMixin
from .object import ObjectMixin
from .form import FormMixin
from .modelform import ModelFormMixin


class ObjectFormMixin(ObjectMixin, ModelMixin, FormMixin):
    def get_form_valid_message(self):
        return f'{self.title}: {self.object}'


class ObjectModelFormMixin(ObjectMixin, ModelFormMixin):
    def get_form_valid_message(self):
        return f'{self.title}: {self.object}'