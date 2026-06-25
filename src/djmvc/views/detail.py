from django.views import generic
from django.utils.html import mark_safe

from ..view import ViewMixin
from ..model import ModelMixin
from .template import TemplateMixin


class DetailView(ModelMixin, TemplateMixin, ViewMixin, generic.DetailView):
    tags = ['object']
    default_template_name = 'detail.html'
    urlpath = '<int:pk>'
    icon = 'eye'
    color = 'primary'
    fields = '__all__'
    exclude = []

    @property
    def title(self):
        return f'{self.object} {self.model._meta.verbose_name.capitalize()} detail'

    @property
    def visible_fields(self):
        return [
            f.name for f in self.model._meta.fields
            if self.fields == '__all__' or f.name not in self.exclude
        ]

    @property
    def display_fields(self):
        return [
            {
                'field': self.model._meta.get_field(field),
                'value': self.get_field_display(field),
                'name': field,
            }
            for field in self.visible_fields
        ]

    def get_field_display(self, name):
        value_getter = '_'.join(['get', name, 'display'])
        if hasattr(self.object, value_getter):
            return getattr(self.object, value_getter)()
        if hasattr(self, value_getter):
            return getattr(self, value_getter)()
        type_getter = '_'.join([
            'get',
            type(self.model._meta.get_field(name)).__name__,
            'display',
        ])
        if hasattr(self, type_getter):
            return getattr(self, type_getter)(name)
        value = getattr(self.object, name)
        if hasattr(value, 'get_absolute_url'):
            return mark_safe(f'''
            <a href="{value.get_absolute_url()}">{value}</a>
            ''')
        return value

    @property
    def model_fields(self):
        obj = getattr(self, 'object', None)
        if not obj:
            return []

        fields = []
        meta = self.model_meta

        for field in meta.get_fields():
            if field.auto_created and not field.concrete:
                continue

            try:
                value = getattr(obj, field.name)

                if value is None:
                    value = '-'
                elif hasattr(value, 'all'):
                    try:
                        value = ', '.join(str(v) for v in value.all())
                    except Exception:
                        value = str(value)
                else:
                    value = str(value)

                fields.append({
                    'label': field.verbose_name.capitalize() if hasattr(field, 'verbose_name') else field.name,
                    'value': value,
                })
            except (AttributeError, ValueError):
                continue

        return fields
