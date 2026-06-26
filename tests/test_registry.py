import pytest
from django.urls import reverse

import djmvc
from djmvc.controller import Controller
from djmvc.registry import Registry
from djmvc.view import View


def test_runtime_register():
    class Extra(View):
        tags = ['navigation']

    class MySite(Controller):
        routes = []

    site = MySite()
    site.routes.register(Extra)
    assert site.routes['extra'].controller is site


def test_register_is_idempotent_by_codename():
    class Extra(View):
        tags = ['navigation']

    class MySite(Controller):
        routes = []

    site = MySite()
    first = site.routes.register(Extra)
    second = site.routes.register(Extra)
    assert len(list(site.routes)) == 1
    assert site.routes['extra'] is second
    assert first is not second


def test_runtime_delete():
    class Home(djmvc.generic.TemplateView):
        pass

    class Extra(djmvc.generic.TemplateView):
        pass

    class MySite(Controller):
        routes = [Home, Extra]

    site = MySite()
    del site.routes['extra']
    assert len(list(site.routes)) == 1
    assert site.routes['home'].controller is site
    with pytest.raises(KeyError):
        site.routes['extra']


def test_whole_entry_swap():
    class Home(djmvc.generic.TemplateView):
        pass

    class Dashboard(djmvc.generic.TemplateView):
        urlpath = ''

    class MySite(Controller):
        routes = [Home]

    site = MySite()
    site.routes['home'] = Dashboard.clone()
    assert site.routes['home'].urlpath == ''


@pytest.mark.urls('djmvc_example.example_urls')
def test_routes_is_registry_not_declaration_list():
    class MySite(Controller):
        routes = [View]

    site = MySite()
    assert isinstance(site.routes, Registry)
    assert not isinstance(site.routes, list)


@pytest.mark.urls('djmvc_example.example_urls')
def test_nested_controller_urlpatterns():
    """Regression: class-level routes= must not shadow cached_property routes."""
    from djmvc_example.example_urls import Site

    site = Site()
    assert isinstance(site.routes, Registry)
    assert reverse('controller:view') == '/controller/view/'
    assert (
        reverse('controller:sub-controller:sub-sub-controller:sub-sub-view')
        == '/controller/sub-controller/sub-sub-controller/sub-sub-view/'
    )