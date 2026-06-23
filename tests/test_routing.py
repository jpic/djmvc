import pytest
from django.urls import reverse


@pytest.mark.urls('djmvc_example.example_urls')
@pytest.mark.parametrize('name,url', (
    ('controller:view', '/controller/view/'),
    ('controller:sub-controller:sub-view', '/controller/sub-controller/sub-view/'),
    (
        'controller:sub-controller:sub-sub-controller:sub-sub-view',
        '/controller/sub-controller/sub-sub-controller/sub-sub-view/',
    ),
))
def test_routing(name, url):
    assert reverse(name) == url


@pytest.mark.urls('djmvc_example.example_urls')
def test_view_controller():
    from djmvc_example.example_urls import Site
    site = Site()

    view = site.routes[0]
    assert view.controller is site
    assert view.controller.root is site
    assert view.url == '/controller/view/'

    sub_view = site.routes[1].routes[0]
    sub_controller = site.routes[1]
    assert sub_view.controller is sub_controller
    assert sub_view.controller.root is site
    assert sub_view.url == '/controller/sub-controller/sub-view/'

    sub_sub_view = site.routes[1].routes[1].routes[0]
    sub_sub_controller = site.routes[1].routes[1]
    assert sub_sub_view.controller is sub_sub_controller
    assert sub_sub_view.controller.root is site
    assert (
        sub_sub_view.url
        == '/controller/sub-controller/sub-sub-controller/sub-sub-view/',
    )
