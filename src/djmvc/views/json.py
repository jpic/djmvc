import json

from django.forms import modelform_factory
from django.http import JsonResponse

JSON_METHODS = ('get', 'post', 'put', 'patch', 'delete')


REST_JSON_METHODS = frozenset({'put', 'patch', 'delete'})


def wants_json(request, method=None):
    """Return whether the client requested a JSON response or body."""
    method = method or request.method.lower()
    if method in REST_JSON_METHODS:
        return True
    accept = request.META.get('HTTP_ACCEPT', '')
    return (
        request.content_type == 'application/json'
        or accept.startswith('application/json')
    )


def json_method_not_allowed(allowed_methods):
    """Build a 405 JSON response listing supported JSON verbs."""
    allowed = ', '.join(m.upper() for m in allowed_methods)
    response = JsonResponse(
        {'detail': 'Method not allowed', 'allowed_methods': list(allowed_methods)},
        status=405,
    )
    response['Allow'] = allowed
    return response


class JsonMixin:
    """Serialize model instances to JSON via the model controller."""

    def get_json_fields(self):
        mc = self.controller.model_controller
        return mc.get_json_fields()

    def serialize(self, obj):
        mc = self.controller.model_controller
        return mc.serialize(obj, self.get_json_fields())


class JsonFormMixin:
    """REST JSON write handlers for model forms (POST / PUT / PATCH)."""

    def get_json_allowed_methods(self):
        return getattr(type(self), 'json_method_names', ('post',))

    def json_method_not_allowed_response(self):
        return json_method_not_allowed(self.get_json_allowed_methods())

    def get_json_body(self):
        if not self.request.body:
            return {}
        return json.loads(self.request.body)

    def get_json_form_class(self, field_names=None):
        if field_names is not None:
            return modelform_factory(self.model, fields=field_names)
        return self.get_form_class()

    def get_json_form_kwargs(self, partial=False):
        data = self.get_json_body()
        kwargs = {'data': data}
        if getattr(self, 'object', None) is not None:
            kwargs['instance'] = self.object
        if partial:
            kwargs['_partial_fields'] = list(data.keys())
        return kwargs

    def build_json_form(self, partial=False):
        kwargs = self.get_json_form_kwargs(partial=partial)
        partial_fields = kwargs.pop('_partial_fields', None)
        if partial and partial_fields is not None:
            form_class = self.get_json_form_class(field_names=partial_fields)
        else:
            form_class = self.get_json_form_class()
        return form_class(**kwargs)

    def json_form_valid_response(self, form):
        self.form = form
        self.object = form.save()
        if hasattr(self, 'log_insert'):
            self.log_insert()
        mc = self.controller.model_controller
        return JsonResponse(
            {
                'data': mc.serialize(self.object),
                'status': 'accepted',
            },
            status=201,
        )

    def json_form_invalid_response(self, form):
        return JsonResponse(
            {
                'status': 'invalid data',
                'non_field_errors': form.non_field_errors(),
                'field_errors': {
                    name: errors for name, errors in form.errors.items()
                },
            },
            status=405,
        )

    def process_json_form(self, partial=False):
        form = self.build_json_form(partial=partial)
        if form.is_valid():
            return self.json_form_valid_response(form)
        return self.json_form_invalid_response(form)

    def json_post(self, request, *args, **kwargs):
        return self.process_json_form(partial=False)

    def json_put(self, request, *args, **kwargs):
        return self.process_json_form(partial=False)

    def json_patch(self, request, *args, **kwargs):
        return self.process_json_form(partial=True)


class JsonDeleteMixin:
    """REST JSON delete handler (DELETE)."""

    def get_json_allowed_methods(self):
        return ('delete',)

    def json_method_not_allowed_response(self):
        return json_method_not_allowed(self.get_json_allowed_methods())

    def json_delete(self, request, *args, **kwargs):
        if not self.can_confirm_delete:
            return JsonResponse(
                {
                    'status': 'protected',
                    'detail': str(self.deletion_protected_message),
                },
                status=409,
            )
        self.log_objects = [self.object]
        if self.object.pk is not None:
            self.object._log_pk = self.object.pk
        self.object.delete()
        self.log_insert()
        return JsonResponse({'status': 'deleted'})