import pytest
from django.contrib.auth import get_user_model

import djmvc

User = get_user_model()


@pytest.fixture(autouse=True)
def _autodiscover_routes():
    """Register per-app routes before tests (same as urls.py, without loading urlconf)."""
    djmvc.site.autodiscover()


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
        assert browser.is_text_present('Logout', wait_time=5), 'Login failed'

    return login