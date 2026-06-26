from ..model import ModelMixin
from .object import ObjectMixin
from .form import FormMixin
from .modelform import ModelFormMixin


class ObjectFormMixin(ObjectMixin, ModelMixin, FormMixin):
    pass


class ObjectModelFormMixin(ObjectMixin, ModelFormMixin):
    pass