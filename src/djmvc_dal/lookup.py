import djmvc
from djmvc.controller import Controller


def find_autocomplete_url(model):
    """Return urlfullname for *model*'s autocomplete route, or None."""
    site = djmvc.site
    if not getattr(site, 'registry', None):
        return None
    return _find_in_tree(site, model)


def _find_in_tree(controller, model):
    for route in controller.routes:
        if isinstance(route, Controller):
            url = _find_in_tree(route, model)
            if url:
                return url
    if getattr(type(controller), 'model', None) is model:
        autocomplete = controller.find_route('autocomplete')
        if autocomplete is not None:
            return autocomplete.urlfullname
    return None