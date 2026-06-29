import operator
from functools import reduce

import djmvc
from django.db.models import Q
from djmvc.controller import Controller


def find_detail_url(model, pk):
    """Return the detail page path for *model*/*pk*, or None."""
    site = djmvc.site
    if not getattr(site, 'registry', None):
        return None
    controller = _find_model_controller(site, model)
    if controller is None:
        return None
    detail = controller.find_route('detail')
    if detail is None:
        return None
    return detail.reverse(pk)


def iter_model_controllers(controller):
    """Yield every :class:`~djmvc.ModelController` under *controller*."""
    for route in controller.routes:
        if not isinstance(route, Controller):
            continue
        if getattr(type(route), 'model', None) is not None:
            yield route
        yield from iter_model_controllers(route)


def iter_searchable_list_views(request):
    """Yield list views the user may search (permission + search_fields)."""
    site = djmvc.site
    if not getattr(site, 'registry', None):
        return
    for controller in iter_model_controllers(site):
        list_route = controller.find_route('list')
        if list_route is None:
            continue
        list_view = type(list_route)(request=request)
        if not list_view.has_permission():
            continue
        if not list_view.search_fields:
            continue
        yield list_view


def get_list_queryset(list_view):
    """Scoped list queryset without the list page ``search`` GET param."""
    qs = list_view.get_scoped_queryset()
    if list_view.filter_fields and list_view.filterset is not None:
        qs = list_view.filterset.qs
    return qs


def apply_search(qs, search_fields, term):
    """Filter *qs* with icontains OR across *search_fields* for *term*."""
    if not search_fields or not term:
        return qs
    return qs.filter(
        reduce(
            operator.or_,
            [Q(**{f'{field}__icontains': term}) for field in search_fields],
        )
    ).distinct()


def _find_model_controller(controller, model):
    for route in controller.routes:
        if isinstance(route, Controller):
            found = _find_model_controller(route, model)
            if found is not None:
                return found
    if getattr(type(controller), 'model', None) is model:
        return controller
    return None