import functools

import django_tables2
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .log import ADDITION, CHANGE, DELETION, format_logentry_message


class ActionsColumn(django_tables2.Column):
    empty_values = ()
    template_name = 'djmvc/_actions_column.html'
    exclude_from_export = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', 'Actions')
        kwargs.setdefault('orderable', False)
        super().__init__(*args, **kwargs)

    def render(self, record, table):
        actions = table.view.controller.get_tagged_views(
            'object',
            request=table.view.request,
            object=record,
        )
        context = {
            'actions': actions,
            'view': table.view,
            'record': record,
        }
        return render_to_string(self.template_name, context, request=table.view.request)


class CheckboxColumn(django_tables2.Column):
    empty_values = ()
    template_name = 'djmvc/_checkbox_column.html'
    exclude_from_export = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', mark_safe(
            render_to_string('djmvc/_checkbox_header.html')
        ))
        kwargs.setdefault('orderable', False)
        super().__init__(*args, **kwargs)

    def render(self, record, table):
        actions = table.view.controller.get_tagged_views(
            'list_action',
            request=table.view.request,
            object=record,
        )
        if not actions:
            return ''
        return render_to_string(
            self.template_name,
            {'record': record},
            request=table.view.request,
        )


class LogActionColumn(django_tables2.Column):
    colors = {
        ADDITION: 'success',
        CHANGE: 'warning',
        DELETION: 'danger',
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', 'Action')
        kwargs.setdefault('orderable', True)
        super().__init__(*args, **kwargs)

    def render(self, value, record=None):
        if record is None:
            return format_html('<span class="tag is-light">{}</span>', value)
        return format_html(
            '<span class="tag is-{}">{}</span>',
            self.colors.get(record.action_flag, 'light'),
            record.get_action_flag_display(),
        )


class LogMessageColumn(django_tables2.Column):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', 'Changes')
        kwargs.setdefault('orderable', False)
        super().__init__(*args, **kwargs)

    def render(self, value):
        return format_logentry_message(value)


class Tables2Mixin:
    table_template = 'djmvc/_tables2.html'

    def _declared_table_fields(self):
        for cls in type(self).__mro__:
            if 'table_fields' in cls.__dict__:
                value = cls.__dict__['table_fields']
                if isinstance(value, list):
                    return list(value)
                break
        return None

    def _auto_table_fields(self):
        all_fields = [
            f.name for f in self.model_meta.get_fields()
            if f.concrete and not f.is_relation
        ]
        pk_field = self.model_meta.pk.name if self.model_meta.pk else 'id'
        fields = [pk_field]

        for f in all_fields:
            if f not in fields and len(fields) < 4:
                fields.append(f)
                if len(fields) == 4:
                    break

        if self.add_actions:
            fields.append('actions')

        return fields

    @functools.cached_property
    def table_fields(self):
        if declared := self._declared_table_fields():
            return declared
        return self._auto_table_fields()

    @functools.cached_property
    def resolved_table_fields(self):
        fields = list(self.table_fields)
        if self.add_checkbox and 'checkbox' not in fields:
            fields.insert(0, 'checkbox')
        return fields

    @functools.cached_property
    def table_meta(self):
        return type(
            'Meta',
            tuple(),
            dict(
                model=self.model,
                fields=self.resolved_table_fields,
                template_name=self.table_template,
            ),
        )

    @functools.cached_property
    def table_class(self):
        attributes = getattr(self, 'table_attributes', {})
        if 'Meta' not in attributes:
            attributes['Meta'] = self.table_meta

        if (
            'actions' in attributes['Meta'].fields
            and 'actions' not in attributes
        ):
            attributes['actions'] = ActionsColumn()

        if (
            'checkbox' in attributes['Meta'].fields
            and 'checkbox' not in attributes
        ):
            attributes['checkbox'] = CheckboxColumn()

        cls = type(
            f'{self.model.__name__}Table',
            (django_tables2.Table,),
            attributes,
        )
        return cls

    @functools.cached_property
    def table(self):
        table = self.table_class(self.object_list)

        table.view = self

        django_tables2.RequestConfig(self.request).configure(table)

        return table

    @functools.cached_property
    def add_actions(self):
        for v in self.controller.routes:
            if 'object' in getattr(v, 'tags', []):
                return True

    @functools.cached_property
    def add_checkbox(self):
        return bool(getattr(self, 'list_actions', []))

    def sort_url(self, column):
        return self.querystring(**{
            self.table.prefixed_order_by_field: column.order_by_alias.next,
        })