import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

import djmvc
from djmvc_dal.lookup import find_autocomplete_url

User = get_user_model()


@pytest.mark.django_db
def test_group_list_route(admin_client, admin_user):
    Group.objects.create(name='editors')
    admin_client.force_login(admin_user)
    response = admin_client.get(reverse('site:auth:group:list'))
    assert response.status_code == 200
    content = response.content.decode()
    assert 'editors' in content


@pytest.mark.django_db
def test_group_autocomplete_route(admin_client, admin_user):
    Group.objects.create(name='editors')
    admin_client.force_login(admin_user)
    response = admin_client.get(
        reverse('site:auth:group:autocomplete'),
        {'q': 'edit'},
    )
    assert response.status_code == 200
    assert b'data-value' in response.content
    assert b'editors' in response.content


@pytest.mark.django_db
def test_find_autocomplete_url_for_user(admin_user):
    url = find_autocomplete_url(User)
    assert url == 'site:auth:user:autocomplete'


@pytest.mark.django_db
def test_find_autocomplete_url_for_group():
    url = find_autocomplete_url(Group)
    assert url == 'site:auth:group:autocomplete'


def test_dal_widget_media_renders_module_scripts():
    from dal import autocomplete

    widget = autocomplete.ModelAlight(url='site:auth:group:autocomplete')
    scripts = ''.join(widget.media.render_js())
    assert 'autocomplete-light.js' in scripts
    assert 'dal-django.js' in scripts
    assert 'type="module"' in scripts


@pytest.mark.django_db
def test_user_update_form_has_groups_autocomplete(admin_client, admin_user):
    user = User.objects.create_user('member', password='pass')
    admin_client.force_login(admin_user)
    response = admin_client.get(
        reverse('site:auth:user:update', args=[user.pk]),
    )
    assert response.status_code == 200
    content = response.content.decode()
    assert 'autocomplete-select' in content
    assert 'autocomplete-light' in content
    assert 'type="module"' in content


@pytest.mark.django_db
def test_user_list_filter_has_groups_autocomplete(admin_client, admin_user):
    admin_client.force_login(admin_user)
    response = admin_client.get(reverse('site:auth:user:list'))
    assert response.status_code == 200
    content = response.content.decode()
    assert 'name="groups"' in content or 'id_groups' in content


@pytest.mark.django_db
def test_filter_groups_narrows_user_list(admin_client, admin_user):
    group = Group.objects.create(name='editors')
    member = User.objects.create_user('member', password='pass')
    member.groups.add(group)
    User.objects.create_user('outsider', password='pass')
    admin_client.force_login(admin_user)
    response = admin_client.get(
        reverse('site:auth:user:list'),
        {'groups': group.pk},
    )
    content = response.content.decode()
    assert 'member' in content
    assert 'outsider' not in content