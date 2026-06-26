import djmvc
import pytest
from django.contrib.auth.models import AnonymousUser

from djmvc.controller import Controller
from djmvc.views import generic
from djmvc_example.stage0.models import Stage0


def _make_request(rf, user):
    request = rf.get('/')
    request.user = user
    return request


@pytest.mark.django_db
def test_find_route_on_immediate_controller(rf, admin_user):
    stage0 = djmvc.site.routes['stage0']
    create_route = stage0.routes['create']
    request = _make_request(rf, admin_user)
    view = type(create_route)(request=request)
    assert view.controller.find_route('list') is stage0.routes['list']


@pytest.mark.django_db
def test_find_route_walks_up_to_parent_controller(rf, admin_user):
    outer = djmvc.ModelController.clone(
        model=Stage0,
        routes=[
            generic.ListView,
            djmvc.Controller.clone(
                codename='nested',
                routes=[
                    djmvc.ModelController.clone(
                        model=Stage0,
                        routes=[generic.CreateView],
                    ),
                ],
            ),
        ],
    )
    site = Controller.clone(codename='site', routes=[outer])()
    site.build()
    inner_mc = site.routes['stage0'].routes['nested'].routes['stage0']
    create_route = inner_mc.routes['create']
    request = _make_request(rf, admin_user)
    view = type(create_route)(request=request)
    assert view.controller.find_route('list') is site.routes['stage0'].routes['list']


@pytest.mark.django_db
def test_list_view_breadcrumbs_empty(rf, admin_user):
    stage0 = djmvc.site.routes['stage0']
    list_route = stage0.routes['list']
    request = _make_request(rf, admin_user)
    view = type(list_route)(request=request)
    assert view.breadcrumbs() == []


@pytest.mark.django_db
def test_create_view_breadcrumbs(rf, admin_user):
    stage0 = djmvc.site.routes['stage0']
    create_route = stage0.routes['create']
    request = _make_request(rf, admin_user)
    view = type(create_route)(request=request)
    crumbs = view.breadcrumbs()
    assert len(crumbs) == 2
    assert type(crumbs[0]).__name__ == 'ListView'
    assert crumbs[1] is view


@pytest.mark.django_db
def test_create_view_breadcrumbs_omits_list_without_permission(rf):
    stage0 = djmvc.site.routes['stage0']
    create_route = stage0.routes['create']
    request = _make_request(rf, AnonymousUser())
    view = type(create_route)(request=request)
    crumbs = view.breadcrumbs()
    assert len(crumbs) == 1
    assert crumbs[0] is view


@pytest.mark.django_db
def test_update_view_breadcrumbs(rf, admin_user):
    obj = Stage0.objects.create(name='Alice')
    stage0 = djmvc.site.routes['stage0']
    update_route = stage0.routes['update']
    request = _make_request(rf, admin_user)
    view = type(update_route)(request=request, object=obj, pk=obj.pk)
    crumbs = view.breadcrumbs()
    assert len(crumbs) == 3
    assert type(crumbs[0]).__name__ == 'ListView'
    assert type(crumbs[1]).__name__ == 'DetailView'
    assert crumbs[1].object == obj
    assert crumbs[2] is view


@pytest.mark.django_db
def test_detail_view_breadcrumbs_without_self(rf, admin_user):
    obj = Stage0.objects.create(name='Alice')
    stage0 = djmvc.site.routes['stage0']
    detail_route = stage0.routes['detail']
    request = _make_request(rf, admin_user)
    view = type(detail_route)(request=request, object=obj, pk=obj.pk)
    crumbs = view.breadcrumbs()
    assert len(crumbs) == 2
    assert type(crumbs[0]).__name__ == 'ListView'
    assert type(crumbs[1]).__name__ == 'DetailView'
    assert crumbs[1].object == obj
    assert view not in crumbs


@pytest.mark.django_db
def test_update_view_breadcrumb_titles(rf, admin_user):
    obj = Stage0.objects.create(name='Alice')
    stage0 = djmvc.site.routes['stage0']
    update_route = stage0.routes['update']
    request = _make_request(rf, admin_user)
    view = type(update_route)(request=request, object=obj, pk=obj.pk)
    crumbs = view.breadcrumbs()
    assert [crumb.breadcrumb_title for crumb in crumbs] == [
        stage0.routes['list'].title,
        str(obj),
        'Update',
    ]


@pytest.mark.django_db
def test_detail_view_titles(rf, admin_user):
    obj = Stage0.objects.create(name='Alice')
    stage0 = djmvc.site.routes['stage0']
    detail_route = stage0.routes['detail']
    request = _make_request(rf, admin_user)
    view = type(detail_route)(request=request, object=obj, pk=obj.pk)
    assert view.title == 'Detail'
    crumbs = view.breadcrumbs()
    assert [crumb.breadcrumb_title for crumb in crumbs] == [
        stage0.routes['list'].title,
        str(obj),
    ]


@pytest.mark.django_db
def test_history_view_titles(rf, admin_user):
    obj = Stage0.objects.create(name='Alice')
    stage0 = djmvc.site.routes['stage0']
    history_route = stage0.routes['history']
    request = _make_request(rf, admin_user)
    view = type(history_route)(request=request, object=obj, pk=obj.pk)
    assert view.title == 'History'
    assert view.breadcrumb_title == 'History'
    crumbs = view.breadcrumbs()
    assert [crumb.breadcrumb_title for crumb in crumbs] == [
        stage0.routes['list'].title,
        str(obj),
        'History',
    ]


@pytest.mark.django_db
def test_object_menu_titles(rf, admin_user):
    obj = Stage0.objects.create(name='Alice')
    stage0 = djmvc.site.routes['stage0']
    history_route = stage0.routes['history']
    request = _make_request(rf, admin_user)
    view = type(history_route)(request=request, object=obj, pk=obj.pk)
    menu = view.controller.model_controller.get_tagged_views(
        'object',
        request=request,
        object=obj,
    )
    assert {item.title for item in menu} == {
        'Detail',
        'Update',
        'Delete',
        'History',
    }