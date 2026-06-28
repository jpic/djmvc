import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse

import djmvc
from djmvc.views.update import UpdateView
from djmvc_example.stage0.models import Item


def grant_perm(user, app_label, codename):
    content_type = ContentType.objects.get(app_label=app_label, model=codename.split('_')[-1])
    perm = Permission.objects.get(content_type=content_type, codename=codename)
    user.user_permissions.add(perm)


@pytest.mark.django_db
def test_list_permission_superuser_only_by_default(rf, admin_user):
    user = djmvc.site.routes['item'].routes['list']
    request = rf.get('/item/')
    request.user = admin_user
    view = type(user)(request=request)
    assert view.permission_fullcode == 'stage0.view_item'
    assert view.has_permission() is True

    from djmvc_example.models import User

    regular = User.objects.create_user('regular', password='pass')
    request.user = regular
    view = type(user)(request=request)
    assert view.has_permission() is False


@pytest.mark.django_db
def test_crud_permissions_use_django_defaults(rf, admin_user):
    from djmvc_example.models import User

    regular = User.objects.create_user('editor', password='pass')
    grant_perm(regular, 'stage0', 'change_item')

    stage0 = djmvc.site.routes['item']
    request = rf.get('/item/1/update/')
    request.user = regular
    item = Item.objects.create(name='A')
    view = type(stage0.routes['update'])(request=request, pk=item.pk)
    assert view.permission_fullcode == 'stage0.change_item'
    assert view.has_permission() is True


@pytest.mark.django_db
def test_has_permission_override_bypasses_controller(rf):
    class PublicView(djmvc.View):
        def has_permission(self):
            return True

    request = rf.get('/')
    from django.contrib.auth.models import AnonymousUser

    request.user = AnonymousUser()
    view = PublicView(request=request)
    assert view.has_permission() is True


@pytest.mark.django_db
def test_dispatch_forbidden_for_authenticated_denied(rf, admin_user):
    from djmvc_example.models import User

    regular = User.objects.create_user('regular', password='pass')
    list_route = djmvc.site.routes['item'].routes['list']
    request = rf.get('/item/')
    request.user = regular
    view = type(list_route)(request=request)
    response = view.dispatch(request)
    assert response.status_code == 403
    assert isinstance(response, TemplateResponse)

    from django.contrib.auth.models import AnonymousUser

    request.user = AnonymousUser()
    view = type(list_route)(request=request)
    response = view.dispatch(request)
    assert response.status_code == 302
    assert response.url == resolve_url('/auth/login/') + '?next=/item/'


@pytest.mark.django_db
def test_action_mixin_object_permission(rf, admin_user):
    item = Item.objects.create(name='mine')
    other = Item.objects.create(name='other')

    class RestrictedUpdate(UpdateView):
        def has_permission_object(self):
            return self.object.name == 'mine'

    controller = djmvc.ModelController.clone(model=Item, routes=[RestrictedUpdate])()
    controller.build()
    request = rf.get('/')
    request.user = admin_user

    update_route = controller.routes['restrictedupdate']
    view = type(update_route)(request=request)
    view.setup(request, pk=item.pk)
    assert view.has_permission() is True

    view = type(update_route)(request=request)
    view.setup(request, pk=other.pk)
    assert view.has_permission() is False


@pytest.mark.django_db
def test_get_tagged_views_respects_permissions(rf, admin_user):
    from djmvc_example.models import User

    regular = User.objects.create_user('regular', password='pass')
    stage0 = djmvc.site.routes['item']
    request = rf.get('/item/')
    request.user = regular
    views = stage0.get_tagged_views('navigation', request=request)
    assert views == []

    request.user = admin_user
    views = stage0.get_tagged_views('navigation', request=request)
    assert len(views) == 1
    assert type(views[0]).__name__ == 'ListView'


@pytest.mark.django_db
def test_custom_backend_introspects_view(rf):
    from djmvc_example.models import User

    class ViewIntrospectionBackend:
        def authenticate(self, *args):
            return None

        def has_perm(self, user_obj, perm, obj=None):
            if obj is None:
                return False
            return obj.permission_shortcode == 'view'

    reader = User.objects.create_user('reader', password='pass')
    backend = ViewIntrospectionBackend()

    class ItemController(djmvc.ModelController):
        model = Item

    controller = ItemController()
    controller.build()
    request = rf.get('/item/')
    request.user = reader
    view = type(controller.routes['list'])(request=request)

    from unittest.mock import patch

    with patch.object(
        reader,
        'has_perm',
        side_effect=lambda perm, obj=None: backend.has_perm(reader, perm, obj),
    ):
        assert view.has_permission_backend() is True


@pytest.mark.django_db
def test_list_with_view_permission_shortcode(rf):
    from djmvc_example.models import User

    reader = User.objects.create_user('reader', password='pass')
    grant_perm(reader, 'stage0', 'view_item')

    controller = djmvc.ModelController.clone(
        model=Item,
        routes=[djmvc.generic.ListView.clone(permission_shortcode='view')],
    )()
    controller.build()
    request = rf.get('/item/')
    request.user = reader
    view = type(controller.routes['list'])(request=request)
    assert view.permission_fullcode == 'stage0.view_item'
    assert view.has_permission() is True