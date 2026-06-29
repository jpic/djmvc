from django.apps import apps
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views import generic
from django.urls import path

from .clonable import Clonable
from .errors import forbidden_response
from .route import Route
from .views.json import wants_json, json_method_not_allowed, JSON_METHODS
from .views.swagger import SWAGGER_BEARER_SECURITY


class ViewMixin(Clonable, Route):
    """Base behaviour for every djmvc view: permissions, URLs, Unpoly defaults.

    Subclasses and clones inherit :attr:`permission_shortcode` from the class
    body when set; otherwise it falls back to the view :attr:`urlname`.
    """

    @property
    def urlpatterns(self):
        """Single Django URL pattern dispatching to this view class."""
        view_func = type(self).as_view()
        return [
            path(self.urlpath, view_func, name=self.urlname)
        ]

    @property
    def title(self):
        """Human-readable label with the ``View`` suffix removed."""
        return super().title.replace('View', '')

    @property
    def breadcrumb_title(self):
        """Breadcrumb label; defaults to :attr:`title`."""
        return self.title

    @property
    def codename(self):
        """URL segment with the ``view`` suffix removed from the class name."""
        return super().codename.replace('view', '')

    def dispatch(self, request, *args, **kwargs):
        """Redirect anonymous users to login; return 403 when permission denied."""
        if wants_json(request, method=request.method.lower()):
            if not self.has_permission():
                if not request.user.is_authenticated:
                    return JsonResponse(
                        {'detail': _('Authentication required')},
                        status=401,
                    )
                return JsonResponse(
                    {'detail': _('Permission denied')},
                    status=403,
                )
            method = request.method.lower()
            handler_name = f'json_{method}'
            handler = getattr(self, handler_name, None)
            if handler is not None:
                result = handler(request, *args, **kwargs)
                if isinstance(result, dict):
                    return JsonResponse(result)
                return result
            allowed = self.get_json_method_names()
            if allowed:
                return json_method_not_allowed(allowed)
            return JsonResponse({'detail': _('Method not allowed')}, status=405)

        if not self.has_permission():
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login

                return redirect_to_login(request.get_full_path())
            return forbidden_response(request, view=self)
        return super().dispatch(request, *args, **kwargs)

    def get_json_method_names(self):
        """Return HTTP verbs supported by ``json_*`` handlers on this view."""
        names = []
        for method in JSON_METHODS:
            if getattr(type(self), f'json_{method}', None) is not None:
                names.append(method)
        return names

    def get_swagger_path_definition(self):
        """Collect per-method Swagger path definitions."""
        result = {}
        for method in JSON_METHODS:
            getter = getattr(self, f'get_swagger_{method}', None)
            if getter is None:
                continue
            definition = getter()
            if not definition:
                continue
            if 'security' not in definition and apps.is_installed('djmvc_api'):
                definition = dict(definition)
                definition['security'] = SWAGGER_BEARER_SECURITY
            result[method] = definition
        return result

    @property
    def swagger_tags(self):
        model = self._permission_model()
        if model is not None:
            return [model.__name__]
        return []

    @property
    def permission_shortcode(self):
        """Django permission prefix (``add``, ``change``, ``view``, …)."""
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
        """Permission codename, e.g. ``view_document``."""
        model = self._permission_model()
        if not model:
            return self.permission_shortcode
        return f'{self.permission_shortcode}_{model._meta.model_name}'

    @property
    def permission_fullcode(self):
        """Fully qualified permission string, e.g. ``myapp.view_document``."""
        model = self._permission_model()
        if not model:
            return self.permission_codename
        return f'{model._meta.app_label}.{self.permission_codename}'

    def has_permission(self):
        """Return whether the current user may access this view."""
        controller = getattr(self, 'controller', None)
        if controller is not None:
            return controller.has_permission(self)
        return self.has_permission_backend()

    def has_permission_backend(self):
        """Check Django permissions, then view-aware custom backends."""
        user = self.request.user
        if user.has_perm(self.permission_fullcode):
            return True
        return user.has_perm(self.permission_fullcode, self)

    def breadcrumbs(self, with_self=True):
        """Return breadcrumb trail; override in object views."""
        return []

    def unpoly_attributes(self, context=None):
        """HTML attributes for Unpoly navigation on this view."""
        return {
            'up-follow': True,
            'up-target': '[up-main]',
        }

    def querystring(self, **params):
        """Current GET query string with *params* merged in."""
        qs = self.request.GET.copy()
        for key, value in params.items():
            qs[key] = value
        return '?' + qs.urlencode()


class View(ViewMixin, generic.View):
    """Minimal djmvc view for custom non-generic handlers."""
    pass