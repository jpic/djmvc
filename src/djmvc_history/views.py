import django_tables2
import djmvc
from django.contrib.admin.models import LogEntry
from djmvc.views.generic import DetailListView, DetailView, ListView
from djmvc.views.tables2 import (
    LogActionColumn,
    LogMessageColumn,
    _logentry_field_verbose_name,
)

from .log import logentries_for


class HistoryView(DetailListView):
    icon = 'clock-history'
    color = 'info'
    filter_fields = []
    search_fields = []

    table_fields = ['action_time', 'user', 'action_flag', 'change_message']
    table_attributes = dict(
        action_time=django_tables2.DateTimeColumn(
            verbose_name=_logentry_field_verbose_name('action_time'),
        ),
        user=django_tables2.Column(accessor='user'),
        action_flag=LogActionColumn(),
        change_message=LogMessageColumn(),
    )

    def get_queryset(self):
        return logentries_for(self.model, self.kwargs['pk'])


class LogEntryController(djmvc.ModelController):
    model = LogEntry

    @property
    def title(self):
        return LogEntry._meta.verbose_name_plural

    routes = [
        ListView.clone(
            table_fields=[
                'action_time',
                'user',
                'content_type',
                'object_repr',
                'action_flag',
                'change_message',
            ],
            table_attributes=dict(
                action_time=django_tables2.DateTimeColumn(
                    verbose_name=_logentry_field_verbose_name('action_time'),
                ),
                user=django_tables2.Column(accessor='user'),
                content_type=django_tables2.Column(accessor='content_type'),
                object_repr=django_tables2.Column(),
                action_flag=LogActionColumn(),
                change_message=LogMessageColumn(),
            ),
            icon='journal-text',
        ),
        DetailView.clone(
            fields=[
                'action_time',
                'user',
                'content_type',
                'object_id',
                'object_repr',
                'action_flag',
                'change_message',
            ],
            icon='journal-text',
        ),
    ]