"""Swagger 2.0 path definition helpers for JSON API views."""

SWAGGER_BEARER_SECURITY = [{'BearerAuth': []}]


def swagger_read_response(model):
    return {
        '200': {
            'description': 'successful operation',
            'schema': {'$ref': f'#/definitions/{model.__name__}'},
        },
    }


def swagger_list_response(model):
    return {
        '200': {
            'description': 'successful operation',
            'schema': {
                'type': 'object',
                'properties': {
                    'results': {
                        'type': 'array',
                        'items': {'$ref': f'#/definitions/{model.__name__}'},
                    },
                    'paginator': {'type': 'object'},
                },
            },
        },
    }


def swagger_json_operation(view, summary, **extra):
    operation = {
        'produces': ['application/json'],
        'summary': summary,
        'tags': view.swagger_tags,
    }
    operation.update(extra)
    return operation


def swagger_body_parameter(view):
    return [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': f'#/definitions/{view.model.__name__}'},
    }]


def swagger_write_operation(view, summary):
    return swagger_json_operation(
        view,
        summary,
        consumes=['application/json'],
        parameters=swagger_body_parameter(view),
        responses={
            '201': {'description': 'Created'},
            '405': {'description': 'Invalid input'},
        },
    )