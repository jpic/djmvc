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

    @property
    def permission_shortcode(self):
        for cls in type(self).__mro__:
            value = cls.__dict__.get('permission_shortcode')
            if isinstance(value, str):
                return value
        return self.urlname

    def _permission_model(self):
        controller = getattr(self, 'controller', None)
        if controller is None:
            return None
        mc = getattr(controller, 'model_controller', controller)
        return getattr(mc, 'model', None)

    @property
    def permission_codename(self):
        model = self._permission_model()
        if not model:
            return self.permission_shortcode
        return f'{self.permission_shortcode}_{model._meta.model_name}'

    @property
    def permission_fullcode(self):
        model = self._permission_model()
        if not model:
            return self.permission_codename
        return f'{model._meta.app_label}.{self.permission_codename}'

    def has_permission(self):
        controller = getattr(self, 'controller', None)
        if controller is not None:
            return controller.has_permission(self)
        return self.has_permission_backend()

    def has_permission_backend(self):
        user = self.request.user
        # ModelBackend ignores user perms when obj is set; check codenames first.
        if user.has_perm(self.permission_fullcode):
            return True
        # View-aware backends (introspect self, like crudlfap blog AuthBackend).
        return user.has_perm(self.permission_fullcode, self)

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
