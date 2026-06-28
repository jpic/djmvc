import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

import djmvc

User = get_user_model()


def grant_model_perm(user, model, action):
    """Grant a default Django model permission (add, change, delete, view)."""
    content_type = ContentType.objects.get_for_model(model)
    codename = f'{action}_{model._meta.model_name}'
    perm = Permission.objects.get(content_type=content_type, codename=codename)
    user.user_permissions.add(perm)


@pytest.fixture(autouse=True)
def _autodiscover_routes():
    """Register per-app routes before tests (same as urls.py, without loading urlconf)."""
    djmvc.site.build()


@pytest.fixture
def stage0_bulk_items(db):
    from djmvc_example.stage0.models import Item

    return [Item.objects.create(name=f'item-{i}') for i in range(4)]


@pytest.fixture
def many_users(db):
    """Enough users to paginate and filter in browser tests."""
    return [
        User.objects.create_user(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password='testpass123',
        )
        for i in range(50)
    ]


@pytest.fixture
def browser_login(browser, live_server):
    def login(username='admin', password='password'):
        browser.visit(f'{live_server.url}/auth/login/')
        browser.fill('username', username)
        browser.fill('password', password)
        browser.find_by_css('button[type="submit"]').first.click()
        assert browser.is_text_present('Log out', wait_time=5), 'Login failed'

    return login