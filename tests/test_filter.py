"""Tests for list filter form."""
import time
from urllib.parse import parse_qs, urlparse

import pytest
from django import forms
from django.template import Context, Template
from django.views import generic

from djmvc.view import ViewMixin
from djmvc.views.filter import FilterMixin
from djmvc.views.list import ListMixin
from djmvc.views.template import TemplateViewMixin
from djmvc.model import ModelMixin
from djmvc_example.stage0.models import Item


def _wait_for_url_without(browser, substring, timeout=5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if substring not in browser.url:
            return
        time.sleep(0.1)
    raise AssertionError(f'{substring!r} still in {browser.url!r}')


class _MockController:
    model = Item
    codename = 'item'
    controller = None
    routes = []

    def find_route(self, codename):
        return None


def _build_filter_view(**attrs):
    return type(
        'TestFilterView',
        (ListMixin, FilterMixin, TemplateViewMixin, ModelMixin, generic.ListView),
        attrs,
    )


@pytest.fixture
def mock_controller():
    return _MockController()


@pytest.mark.django_db
def test_search_auto_added_to_filter_field_names(rf, admin_user, mock_controller):
    view_cls = _build_filter_view()
    request = rf.get('/')
    request.user = admin_user
    view = view_cls()
    view.controller = mock_controller
    view.setup(request)

    assert view.get_filter_field_names() == ['search']
    assert 'search' in view.filter_form.fields


@pytest.mark.django_db
def test_filter_fields_extend_defaults(rf, admin_user, mock_controller):
    view_cls = _build_filter_view(filter_fields=['name'])
    request = rf.get('/')
    request.user = admin_user
    view = view_cls()
    view.controller = mock_controller
    view.setup(request)

    assert view.get_filter_field_names() == ['search', 'name']
    assert 'name' in view.filter_form.fields


@pytest.mark.django_db
def test_no_filter_form_without_fields(rf, admin_user, mock_controller):
    view_cls = _build_filter_view()
    request = rf.get('/')
    request.user = admin_user
    view = view_cls()
    view.controller = mock_controller
    view.setup(request)
    view.search_fields = []

    assert view.get_filter_field_names() == []
    assert view.filter_form is None


@pytest.mark.django_db
def test_filter_fields_without_search(rf, admin_user, mock_controller):
    view_cls = _build_filter_view(filter_fields=['name'])
    request = rf.get('/')
    request.user = admin_user
    view = view_cls()
    view.controller = mock_controller
    view.setup(request)
    view.search_fields = []

    assert view.get_filter_field_names() == ['name']
    assert 'search' not in view.filter_form.fields


@pytest.mark.django_db
def test_filter_form_class_override(rf, admin_user, mock_controller):
    class CustomFilterForm(forms.Form):
        q = forms.CharField(required=False)

    view_cls = _build_filter_view(filter_form_class=CustomFilterForm)
    request = rf.get('/')
    request.user = admin_user
    view = view_cls()
    view.controller = mock_controller
    view.setup(request)

    assert type(view.filter_form) is CustomFilterForm


@pytest.mark.django_db
def test_filter_attributes_include_history(rf, admin_user, mock_controller):
    view_cls = _build_filter_view()
    request = rf.get('/')
    request.user = admin_user
    view = view_cls()
    view.controller = mock_controller
    view.setup(request)

    assert view.filter_attributes['up-history'] is True
    assert view.filter_target == '[up-list]'


@pytest.mark.django_db
def test_has_active_filters_and_clear_url(rf, admin_user, mock_controller):
    view_cls = _build_filter_view()
    request = rf.get('/?search=foo&page=2&per_page=10')
    request.user = admin_user
    view = view_cls()
    view.controller = mock_controller
    view.setup(request)

    assert view.has_active_filters is True
    url = view.clear_filter_url()
    params = parse_qs(urlparse(url).query)
    assert urlparse(url).path == '/'
    assert 'search' not in params
    assert 'page' not in params
    assert params.get('per_page') == ['10']


@pytest.mark.django_db
def test_filter_form_renders_horizontally(rf, admin_user, mock_controller):
    view_cls = _build_filter_view()
    request = rf.get('/')
    request.user = admin_user
    view = view_cls()
    view.controller = mock_controller
    view.setup(request)

    template = Template('''
    {% load djmvc crispy_forms_tags %}
    {% include "djmvc/_filter.html" %}
    ''')
    output = template.render(Context({'view': view, 'request': request}))
    assert 'field is-grouped' in output
    assert 'method="get"' in output
    assert 'name="search"' in output
    assert 'type="submit"' in output
    assert 'method="undefined"' not in output


@pytest.mark.django_db
def test_search_filters_queryset(rf, admin_user, mock_controller, db):
    Item.objects.create(name='alpha')
    Item.objects.create(name='beta')
    view_cls = _build_filter_view()
    request = rf.get('/?search=alpha')
    request.user = admin_user
    view = view_cls()
    view.controller = mock_controller
    view.setup(request)

    names = list(view.get_queryset().values_list('name', flat=True))
    assert names == ['alpha']


@pytest.mark.django_db
def test_filter_form_method_is_get(rf, admin_user, mock_controller):
    """Regression: form method must be 'get', not leaked context named 'method'."""
    import djmvc

    list_route = djmvc.site.routes['auth'].routes['user'].routes['list']
    request = rf.get('/auth/user/?search=foo')
    request.user = admin_user
    view = type(list_route)()
    view.setup(request)
    view.object_list = view.get_queryset()

    template = Template('''
    {% load djmvc crispy_forms_tags django_tables2 %}
    {% render_table view.table 'djmvc/_tables2.html' %}
    ''')
    output = template.render(Context({'view': view, 'request': request}))
    assert 'up-list' in output
    assert 'method="get"' in output
    assert 'method="undefined"' not in output
    assert 'Clear' in output


@pytest.mark.splinter(screenshot_dir='./screenshots')
@pytest.mark.django_db
def test_filter_search_on_user_list(
    browser, live_server, browser_login, admin_user, many_users,
):
    browser_login()
    browser.visit(f'{live_server.url}/auth/user/')

    form = browser.find_by_css('form.djmvc-filter-form').first
    assert form['method'] == 'get'

    search_input = browser.find_by_css(
        'form.djmvc-filter-form input[name="search"]',
    ).first
    search_input.fill('user42')
    browser.find_by_css('form.djmvc-filter-form button[type="submit"]').first.click()

    assert browser.is_element_present_by_css('[up-list]', wait_time=5)
    assert 'search=user42' in browser.url
    assert browser.is_text_present('user42', wait_time=5)

    table_text = browser.find_by_css('[up-table]').first.text
    assert 'user42' in table_text
    assert 'user0' not in table_text
    assert browser.find_by_css('input[name="search"]').first.value == 'user42'
    assert browser.is_text_present('Clear', wait_time=2)


@pytest.mark.splinter(screenshot_dir='./screenshots')
@pytest.mark.django_db
def test_filter_clear_on_user_list(
    browser, live_server, browser_login, admin_user, many_users,
):
    browser_login()
    browser.visit(f'{live_server.url}/auth/user/?search=user42')

    assert browser.is_element_present_by_css(
        'form.djmvc-filter-form .djmvc-filter-clear',
        wait_time=5,
    )
    browser.find_by_css('form.djmvc-filter-form .djmvc-filter-clear').first.click()

    assert browser.is_element_present_by_css('[up-list]', wait_time=5)
    _wait_for_url_without(browser, 'search=')
    assert browser.is_text_present('user0', wait_time=5)
    assert browser.find_by_css('input[name="search"]').first.value == ''