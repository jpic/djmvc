from django.views import generic
from django.urls import path

from .clonable import Clonable
from .route import Route


class ViewMixin(Clonable, Route):
    @property
    def urlpatterns(self):
        view_func = type(self).as_view()
        return [
            path(self.urlpath, view_func, name=self.urlname)
        ]

    @property
    def name(self):
        return super().name.replace('View', '')

    @property
    def codename(self):
        return super().codename.replace('view', '')


class View(ViewMixin, generic.View):
    def has_permission(self):
        return self.request.user.is_superuser
