from djmvc.views.generic import TemplateView
from djmvc_example.urls import site


def test_get_context_data():
    view = TemplateView()
    assert view.get_context_data()['view'] is view


def test_get_template_names():
    assert site.routes['auth'].routes['login'].get_template_names() == [
        'djmvc/auth/login.html',
        'djmvc/example_project/auth/login.html',
        'djmvc/form.html',
        'auth/login.html',
        'example_project/auth/login.html',
        'form.html',
    ]
