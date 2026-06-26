import djmvc
import pytest
from django.template import Context, Template
from django.test import RequestFactory

from djmvc.templatetags.djmvc import html_attributes, unpoly_attributes
from djmvc.views import generic
from djmvc_example.stage0.models import Stage0


def test_html_attributes_renders_key_value_pairs():
    assert html_attributes({'up-layer': 'new modal'}) == 'up-layer="new modal"'


def test_html_attributes_renders_boolean_true():
    assert html_attributes({'up-submit': True}) == 'up-submit'


def test_html_attributes_escapes_values():
    result = html_attributes({'data-x': '"<&>'})
    assert result == 'data-x="&quot;&lt;&amp;&gt;"'


def test_html_attributes_skips_malformed_keys():
    assert html_attributes({'foo" onclick': 'x'}) == ''


def test_unpoly_attributes_filter_for_form_view():
    rf = RequestFactory()
    request = rf.get('/stage0/')
    stage0 = djmvc.site.routes['stage0']
    create_route = stage0.routes['create']
    view = type(create_route)(request=request)
    attrs = unpoly_attributes(view, 'model_menu')
    assert attrs['up-layer'] == 'new modal'
    assert attrs['up-accept-location'] == '/stage0/'


def test_unpoly_attributes_filter_without_method():
    rf = RequestFactory()
    request = rf.get('/stage0/1/detail/')
    stage0 = djmvc.site.routes['stage0']
    detail_route = stage0.routes['detail']
    obj = Stage0(name='x')
    view = type(detail_route)(request=request, object=obj, pk=1)
    assert unpoly_attributes(view, 'object_menu') == {}


def test_unpoly_attributes_filter_in_template():
    template = Template(
        '{% load djmvc %}'
        '{{ view|unpoly_attributes:"model_menu"|html_attributes }}'
    )
    rf = RequestFactory()
    request = rf.get('/stage0/')
    stage0 = djmvc.site.routes['stage0']
    create_route = stage0.routes['create']
    view = type(create_route)(request=request)
    output = template.render(Context({'view': view}))
    assert 'up-layer="new modal"' in output
    assert 'up-accept-location="/stage0/"' in output