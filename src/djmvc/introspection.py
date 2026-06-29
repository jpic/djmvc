import re

import djmvc

from .controller import Controller


def compute_fullurlpath(route):
    """Return the URL path for *route* by walking controller ancestors."""
    try:
        return route.url
    except Exception:
        parts = []
        current = route
        while current is not None:
            segment = getattr(current, 'urlpath', '')
            if segment:
                parts.insert(0, segment.strip('/'))
            current = getattr(current, 'controller', None)
        if not parts:
            return '/'
        return '/' + '/'.join(parts) + '/'


def swagger_path(fullurlpath):
    """Convert Django URL path converters to Swagger brace syntax."""
    return '/' + re.sub(r'<(?:[^:>]+:)?([^>]+)>', r'{\1}', fullurlpath.strip('/'))


def walk_leaf_views(controller):
    """Yield built view route instances under *controller*."""
    routes = getattr(controller, 'routes', None)
    if routes is None:
        return
    for route in routes:
        if isinstance(route, Controller):
            yield from walk_leaf_views(route)
        else:
            yield route


def walk_model_controllers(controller):
    """Yield :class:`~djmvc.ModelController` instances in the tree."""
    if getattr(type(controller), 'model', None) is not None:
        yield controller
    routes = getattr(controller, 'routes', None)
    if routes is None:
        return
    for route in routes:
        if isinstance(route, Controller):
            yield from walk_model_controllers(route)


def get_built_site(site):
    """Return *site* after :meth:`~djmvc.Site.build` if needed."""
    if not hasattr(site, 'registry'):
        site.build()
    return site


def has_json_handler(view_class):
    """Return whether *view_class* defines any ``json_*`` handler."""
    return any(
        hasattr(view_class, f'json_{method}')
        for method in ('get', 'post', 'put', 'patch', 'delete')
    )


def instantiate_view(route, request):
    """Return a view instance bound to *request* from a built route."""
    view = type(route)(request=request)
    view.args = ()
    view.kwargs = {}
    return view


def iter_schema_json_views(request, site=None):
    """Yield every JSON-capable view for Swagger schema (no permission filter)."""
    site = get_built_site(site or djmvc.site)
    for route in walk_leaf_views(site):
        if has_json_handler(type(route)):
            yield instantiate_view(route, request)


def iter_schema_model_controllers(request, site=None):
    """Yield model controllers referenced by JSON-capable views in the schema."""
    seen = set()
    for view in iter_schema_json_views(request, site):
        mc = view.controller.model_controller
        if getattr(type(mc), 'model', None) is None:
            continue
        key = id(mc)
        if key not in seen:
            seen.add(key)
            yield mc