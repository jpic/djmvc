from django.template.response import TemplateResponse


DEFAULT_ERROR_PAGES = {
    400: (
        'Bad request',
        'The request could not be understood by the server.',
    ),
    403: (
        'Forbidden',
        'You do not have permission to access this page.',
    ),
    404: (
        'Not found',
        'The page you requested could not be found.',
    ),
    500: (
        'Server error',
        'Something went wrong on our end. Please try again later.',
    ),
}


def layout_view_for_request(request):
    import djmvc
    from .views.template import TemplateView

    if not hasattr(djmvc.site, 'registry'):
        djmvc.site.build()

    class LayoutView(TemplateView):
        def has_permission(self):
            return True

    view_class = LayoutView.clone(controller=djmvc.site)
    view = view_class()
    view.request = request
    view.kwargs = {}
    view.args = ()
    return view


def error_response(request, status, view=None, title=None, message=None):
    view = view or layout_view_for_request(request)
    default_title, default_message = DEFAULT_ERROR_PAGES[status]
    context = {
        'view': view,
        'error_status': status,
        'error_title': title or default_title,
        'error_message': message or default_message,
    }
    return TemplateResponse(
        request,
        [
            f'djmvc/{status}.html',
            'djmvc/error.html',
            f'{status}.html',
        ],
        context,
        status=status,
    )


def bad_request_response(request, view=None, title=None, message=None):
    return error_response(request, 400, view=view, title=title, message=message)


def forbidden_response(request, view=None, title=None, message=None):
    return error_response(request, 403, view=view, title=title, message=message)


def not_found_response(request, view=None, title=None, message=None):
    return error_response(request, 404, view=view, title=title, message=message)


def server_error_response(request, view=None, title=None, message=None):
    return error_response(request, 500, view=view, title=title, message=message)