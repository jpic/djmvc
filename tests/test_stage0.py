import pytest
from django.forms import ModelForm
from django.urls import reverse

from djmvc_example.stage0.models import Stage0


@pytest.mark.django_db
def test_stage0_create_get_renders_model_form(client, admin_user):
    client.force_login(admin_user)

    response = client.get(reverse('site:stage0:create'))

    assert response.status_code == 200
    assert isinstance(response.context['form'], ModelForm)
    assert 'name' in response.context['form'].fields


@pytest.mark.django_db
def test_stage0_crud(client, admin_user):
    client.force_login(admin_user)

    assert client.get(reverse('site:stage0:create')).status_code == 200
    client.post(reverse('site:stage0:create'), {'name': 'Alice'})
    obj = Stage0.objects.get(name='Alice')

    list_response = client.get(reverse('site:stage0:list'))
    assert list_response.status_code == 200
    assert b'Alice' in list_response.content

    assert client.get(reverse('site:stage0:detail', args=[obj.pk])).status_code == 200

    client.post(reverse('site:stage0:update', args=[obj.pk]), {'name': 'Bob'})
    obj.refresh_from_db()
    assert obj.name == 'Bob'

    assert client.get(reverse('site:stage0:delete', args=[obj.pk])).status_code == 200
    client.post(reverse('site:stage0:delete', args=[obj.pk]))
    assert not Stage0.objects.filter(pk=obj.pk).exists()


@pytest.mark.django_db
def test_stage0_bulk_delete(client, admin_user):
    client.force_login(admin_user)
    client.post(reverse('site:stage0:create'), {'name': 'A'})
    client.post(reverse('site:stage0:create'), {'name': 'B'})
    a = Stage0.objects.get(name='A')
    b = Stage0.objects.get(name='B')

    url = reverse('site:stage0:deleteobjects') + f'?pks={a.pk}&pks={b.pk}'
    assert client.get(url).status_code == 200
    client.post(url, {'next': reverse('site:stage0:list')})
    assert Stage0.objects.count() == 0