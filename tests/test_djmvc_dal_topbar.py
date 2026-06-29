import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from djmvc_dal_topbar.lookup import find_detail_url

User = get_user_model()


@pytest.mark.django_db
def test_site_search_route(admin_client, admin_user):
    User.objects.create_user('member', password='pass')
    admin_client.force_login(admin_user)
    response = admin_client.get(reverse('site:search'), {'q': 'member'})
    assert response.status_code == 200
    content = response.content.decode()
    assert 'member' in content
    assert 'data-url' in content
    assert '/detail/' in content


@pytest.mark.django_db
def test_find_detail_url_for_user(admin_user):
    user = User.objects.create_user('member', password='pass')
    url = find_detail_url(User, user.pk)
    assert url == reverse('site:auth:user:detail', args=[user.pk])


@pytest.mark.django_db
def test_site_search_excludes_models_without_list_permission(db, client):
    user = User.objects.create_user('viewer', password='pass')
    User.objects.create_user('member', password='pass')
    client.force_login(user)
    response = client.get(reverse('site:search'), {'q': 'member'})
    assert response.status_code == 200
    assert b'member' not in response.content


@pytest.mark.django_db
def test_pages_include_site_search_widget(admin_client, admin_user):
    admin_client.force_login(admin_user)
    response = admin_client.get(reverse('site:auth:user:list'))
    content = response.content.decode()
    assert 'djmvc-site-search' in content
    assert reverse('site:search') in content
    assert 'djmvc-site-search-wrap' in content
    assert 'slot="input"' in content