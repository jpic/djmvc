import pytest
from django.http import Http404

import djmvc
from djmvc.views.delete import DeleteObjectsView
from djmvc_example.stage0.models import Stage0


@pytest.mark.django_db
def test_controller_get_queryset_scopes_list(rf, admin_user):
    owned = Stage0.objects.create(name='owned')
    Stage0.objects.create(name='other')

    class Stage0Controller(djmvc.ModelController):
        model = Stage0

        def get_queryset(self, view):
            return self.model.objects.filter(name='owned')

    controller = Stage0Controller()
    controller.build()
    request = rf.get('/stage0/')
    request.user = admin_user
    view = type(controller.routes['list'])(request=request)
    view.setup(request)
    assert list(view.get_queryset().values_list('name', flat=True)) == ['owned']


@pytest.mark.django_db
def test_get_object_404_outside_scoped_queryset(rf, admin_user):
    owned = Stage0.objects.create(name='owned')
    other = Stage0.objects.create(name='other')

    class Stage0Controller(djmvc.ModelController):
        model = Stage0

        def get_queryset(self, view):
            return self.model.objects.filter(name='owned')

    controller = Stage0Controller()
    controller.build()
    request = rf.get(f'/stage0/{other.pk}/detail/')
    request.user = admin_user
    view = type(controller.routes['detail'])(request=request)
    with pytest.raises(Http404):
        view.setup(request, pk=other.pk)


@pytest.mark.django_db
def test_get_object_returns_scoped_object(rf, admin_user):
    owned = Stage0.objects.create(name='owned')

    class Stage0Controller(djmvc.ModelController):
        model = Stage0

        def get_queryset(self, view):
            return self.model.objects.filter(name='owned')

    controller = Stage0Controller()
    controller.build()
    request = rf.get(f'/stage0/{owned.pk}/detail/')
    request.user = admin_user
    view = type(controller.routes['detail'])(request=request)
    view.setup(request, pk=owned.pk)
    assert view.object.pk == owned.pk


@pytest.mark.django_db
def test_list_action_intersects_scoped_queryset(rf, admin_user):
    a = Stage0.objects.create(name='owned')
    b = Stage0.objects.create(name='other')

    class Stage0Controller(djmvc.ModelController):
        model = Stage0
        routes = djmvc.ModelController.routes

        def get_queryset(self, view):
            return self.model.objects.filter(name='owned')

    controller = Stage0Controller()
    controller.build()
    request = rf.get(f'/stage0/deleteobjects/?pks={a.pk}&pks={b.pk}')
    request.user = admin_user
    view = type(controller.routes['deleteobjects'])(request=request)
    assert list(view.object_list.values_list('pk', flat=True)) == [a.pk]
    assert view.invalid_pks == 1