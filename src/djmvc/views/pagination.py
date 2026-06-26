import functools

from django.core.paginator import InvalidPage
from django.http import Http404
from django.utils.translation import gettext as _


class PaginationMixin:
    paginate_by = 25
    per_page_options = '10,25,50,100'
    page_kwarg = 'page'
    per_page_kwarg = 'per_page'
    pagination_target = '[up-list]'

    def get_paginate_by(self, queryset=None):
        if self.paginate_by is None:
            return None
        return self.resolved_per_page

    @functools.cached_property
    def resolved_per_page(self):
        allowed = {int(x) for x in self.per_page_options.split(',')}
        raw = self.request.GET.get(self.per_page_kwarg)
        if raw is not None and raw.isdigit():
            value = int(raw)
            if value in allowed:
                return value
        return self.paginate_by

    @property
    def page(self):
        page_obj = getattr(self, 'page_obj', None)
        if page_obj is not None:
            return page_obj
        return None

    @property
    def paginator(self):
        page = self.page
        if page is not None:
            return page.paginator
        return getattr(self, '_paginator', None)

    def pagination_url(self, page_number):
        return self.querystring(**{self.page_kwarg: str(page_number)})

    @property
    def pagination_form_attributes(self):
        return {
            'up-submit': True,
            'up-target': self.pagination_target,
            'up-history': True,
            'up-autosubmit': True,
        }

    def pagination_hidden_fields(self, *exclude):
        excluded = set(exclude)
        for key, values in self.request.GET.lists():
            if key in excluded:
                continue
            for value in values:
                yield key, value

    @property
    def per_page_option_list(self):
        return self.per_page_options.split(',')

    @property
    def per_page_form_hidden_fields(self):
        return list(self.pagination_hidden_fields(
            self.per_page_kwarg,
            self.page_kwarg,
        ))

    @property
    def page_form_hidden_fields(self):
        return list(self.pagination_hidden_fields(self.page_kwarg))

    def clamp_page_number(self, page_number, paginator):
        num_pages = paginator.num_pages
        if num_pages < 1:
            return 1
        return min(max(page_number, 1), num_pages)

    def get_requested_page_number(self, paginator):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            return int(page)
        except (TypeError, ValueError):
            if page == 'last':
                return paginator.num_pages or 1
            raise Http404(
                _('Page is not “last”, nor can it be converted to an int.'),
            )

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page_number = self.clamp_page_number(
            self.get_requested_page_number(paginator),
            paginator,
        )
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            page_number = self.clamp_page_number(page_number, paginator)
            page = paginator.page(page_number)
        self.page_obj = page
        self._paginator = paginator
        return paginator, page, page.object_list, page.has_other_pages()