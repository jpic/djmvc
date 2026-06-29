import json
from datetime import timedelta

import djmvc
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

from djmvc.introspection import (
    compute_fullurlpath,
    get_built_site,
    iter_schema_json_views,
    iter_schema_model_controllers,
    swagger_path,
)
from djmvc.view import View
from djmvc.views.json import json_method_not_allowed
from djmvc.views.template import TemplateView

from .models import Token

API_LOGIN_TOKEN_LIFETIME = timedelta(hours=1)
API_LOGIN_TOKEN_NAME = 'API login'


@method_decorator(csrf_exempt, name='dispatch')
class ApiLoginView(View):
    """Exchange username/password for a short-lived Bearer token."""

    urlpath = 'login/'

    def has_permission(self):
        return True

    def _login_response(self, request):
        try:
            data = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            return JsonResponse({'detail': _('Invalid JSON')}, status=400)

        username = data.get('username', '')
        password = data.get('password', '')
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is None:
            return JsonResponse(
                {'detail': _('Invalid username or password')},
                status=401,
            )

        expires = timezone.now() + API_LOGIN_TOKEN_LIFETIME
        token, raw_key = Token.generate(
            user=user,
            name=API_LOGIN_TOKEN_NAME,
            expires=expires,
        )
        return JsonResponse({
            'token': raw_key,
            'expires': expires.isoformat(),
            'prefix': token.prefix,
        })

    def json_post(self, request, *args, **kwargs):
        return self._login_response(request)

    def get_swagger_post(self):
        return {
            'consumes': ['application/json'],
            'produces': ['application/json'],
            'summary': 'Obtain a 1-hour API token',
            'tags': ['Authentication'],
            'security': [],
            'parameters': [{
                'in': 'body',
                'name': 'credentials',
                'required': True,
                'schema': {
                    'type': 'object',
                    'required': ['username', 'password'],
                    'properties': {
                        'username': {'type': 'string'},
                        'password': {'type': 'string'},
                    },
                },
            }],
            'responses': {
                '200': {
                    'description': 'Token issued',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'token': {'type': 'string'},
                            'expires': {'type': 'string', 'format': 'date-time'},
                            'prefix': {'type': 'string'},
                        },
                    },
                },
                '401': {'description': 'Invalid credentials'},
            },
        }


class TokenCreateView(djmvc.generic.CreateView):
    """Create a named API token via HTML form (raw key shown once)."""

    fields = ['name', 'expires']

    def json_post(self, request, *args, **kwargs):
        return json_method_not_allowed(())

    def form_valid(self, form):
        token, raw_key = Token.generate(
            user=self.request.user,
            name=form.cleaned_data['name'],
            expires=form.cleaned_data.get('expires'),
        )
        self.object = token
        messages.success(
            self.request,
            _('Token created: %(key)s — copy it now, it will not be shown again.')
            % {'key': raw_key},
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.controller.find_route('list').reverse()


class TokenController(djmvc.ModelController):
    model = Token
    icon = 'key'
    json_fields = ['id', 'name', 'prefix', 'created', 'expires']

    routes = [
        djmvc.generic.ListView,
        djmvc.generic.DetailView,
        TokenCreateView,
        djmvc.generic.DeleteView,
    ]

    def get_queryset(self, view):
        qs = super().get_queryset(view)
        if view.request.user.is_superuser:
            return qs
        return qs.filter(user=view.request.user)


class SchemaView(View):
    """Serve a Swagger 2.0 schema for JSON-capable routes."""

    urlpath = 'schema/'

    def has_permission(self):
        return True

    def build_schema(self, request):
        schema = {
            'swagger': '2.0',
            'info': {'title': 'djmvc API', 'version': '1.0.0'},
            'host': request.get_host(),
            'basePath': '/',
            'schemes': ['https', 'http'],
            'consumes': ['application/json'],
            'produces': ['application/json'],
            'paths': {},
            'definitions': {},
            'securityDefinitions': {
                'BearerAuth': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'Authorization',
                    'description': (
                        'Use POST /api/login/ (Try it out) to get a token, '
                        'or paste: Bearer <token>'
                    ),
                },
            },
            'tags': [],
        }

        for controller in iter_schema_model_controllers(request):
            model_name = controller.get_swagger_model_name(request)
            if model_name and model_name not in schema['definitions']:
                definition = controller.get_swagger_model_definition(request)
                if definition:
                    schema['definitions'][model_name] = definition

        for view in iter_schema_json_views(request):
            path_definition = view.get_swagger_path_definition()
            if not path_definition:
                continue
            url = swagger_path(compute_fullurlpath(view))
            existing = schema['paths'].setdefault(url, {})
            existing.update(path_definition)

        return schema

    def json_get(self, request, *args, **kwargs):
        return self.build_schema(request)

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.json_get(request, *args, **kwargs))


class SwaggerUIView(TemplateView):
    """Render Swagger UI for the generated schema."""

    urlpath = ''
    default_template_name = 'djmvc_api/api.html'

    def has_permission(self):
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api = get_built_site(djmvc.site).routes['api']
        context['schema_url'] = api.find_route('schema').reverse()
        context['login_url'] = api.find_route('apilogin').reverse()
        return context


class ApiController(djmvc.Controller):
    routes = [
        SwaggerUIView.clone(urlname='swagger', urlpath=''),
        SchemaView.clone(urlname='schema', urlpath='schema/'),
        ApiLoginView.clone(urlname='login', urlpath='login/'),
        TokenController,
    ]