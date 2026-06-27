from django.conf import settings
from django.shortcuts import resolve_url
from django.views import generic
from django.urls import path

from .clonable import Clonable
from .errors import forbidden_response
from .route import Route


class ViewMixin(Clonable, Route):
    @property
    def urlpatterns(self):
        view_func = type(self).as_view()
        return [
            path(self.urlpath, view_func, name=self.urlname)
        ]

    @property
    def title(self):
        return super().title.replace('View', '')

    @property
    def breadcrumb_title(self):
        return self.title

    @property
    def codename(self):
        return super().codename.replace('view', '')

    def dispatch(self, *args, **kwargs):
        if not self.has_permission():
            if not self.request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login

                return redirect_to_login(
                    self.request.get_full_path(),
                )
            else:
                return forbidden_response(self.request, view=self)
        return super().dispatch(*args, **kwargs)

    def has_permission(self):
        return self.request.user.is_superuser

    def breadcrumbs(self, with_self=True):
        return []

    def unpoly_attributes(self, context=None):
        return {
            'up-follow': True,
            'up-target': '[up-main]',
        }

    def querystring(self, **params):
        qs = self.request.GET.copy()
        for key, value in params.items():
            qs[key] = value
        return '?' + qs.urlencode()


class View(ViewMixin, generic.View):
    pass
