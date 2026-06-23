import pytest


@pytest.mark.urls('djmvc_example.example_urls')
def test_routing():
    from django.urls import reverse
    assert reverse('controller:view') == '/controller/view/'
    assert reverse('controller:sub-controller:sub-view') == '/controller/sub-controller/sub-view/'
