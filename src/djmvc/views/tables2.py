import functools
import django_tables2
from django.template.loader import render_to_string

class ActionsColumn(django_tables2.Column):
    empty_values = ()  # Always render column
    template_name = 'djmvc/_actions_column.html'
    exclude_from_export = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', 'Actions')
        kwargs.setdefault('orderable', False)  # Ensure column cannot be sorted
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


class Tables2Mixin:
    table_template = 'djmvc/_tables2.html'

    @functools.cached_property
    def table_fields(self):
        # Get all concrete fields in declaration/ Meta order
        all_fields = [
            f.name for f in self.model_meta.get_fields()
            if f.concrete and not f.is_relation  # avoid relations for basic tables
        ]
        # Ensure 'id' or 'pk' is first if present
        pk_field = self.model_meta.pk.name if self.model_meta.pk else 'id'
        fields = [pk_field]

        # Add up to first 3 other fields (avoiding pk duplicate)
        for f in all_fields:
            if f not in fields and len(fields) < 4:  # id + 3 others = 4 max
                fields.append(f)
                if len(fields) == 4:
                    break

        if self.add_actions:
            fields.append('actions')

        return fields

    @functools.cached_property
    def table_meta(self):
        return type(
            'Meta',
            tuple(),
            dict(
                model=self.model,
                fields=self.table_fields,
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

    def sort_url(self, column):
        return self.querystring(**{
            self.table.prefixed_order_by_field: column.order_by_alias.next,
        })
