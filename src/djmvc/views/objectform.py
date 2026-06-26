from ..model import ModelMixin
from .log import CHANGE
from .object import ObjectMixin
from .form import FormMixin
from .modelform import ModelFormMixin


class ObjectFormMixin(ObjectMixin, ModelMixin, FormMixin):
    def get_form_valid_message(self):
        return f'{self.title}: {self.object}'


class ObjectModelFormMixin(ObjectMixin, ModelFormMixin):
    log_action_flag = CHANGE

    def get_form_valid_message(self):
        return f'{self.title}: {self.object}'