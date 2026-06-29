import pytest
from django.contrib.auth import get_user_model

from alight_helpers import open_autocomplete, type_and_select, wait_alight_ready
from topbar_screenshots import capture, prepare_browser

User = get_user_model()


@pytest.fixture
def grouped_users(db):
    member = User.objects.create_user('member', password='pass')
    outsider = User.objects.create_user('outsider', password='pass')
    return member, outsider


@pytest.mark.splinter(screenshot_dir='./screenshots')
@pytest.mark.django_db
def test_site_search_navigates_to_user_detail(
    browser,
    live_server,
    browser_login,
    admin_user,
    grouped_users,
):
    member, _ = grouped_users
    browser_login()
    browser.visit(f'{live_server.url}/auth/user/')

    wait_alight_ready(browser)
    assert browser.is_element_present_by_css('.djmvc-site-search', wait_time=5)

    prepare_browser(browser)
    capture(browser, 'site-search-initial')

    open_autocomplete(browser, '.djmvc-site-search input')
    browser.find_by_css('.djmvc-site-search input').first.type('member')
    assert browser.is_element_present_by_css(
        '.autocomplete-light-box [data-value]',
        wait_time=5,
    )
    capture(browser, 'site-search-results')

    type_and_select(
        browser,
        'member',
        container_css='.djmvc-site-search',
        input_css='.djmvc-site-search input',
    )

    assert browser.is_element_present_by_css('[up-main]', wait_time=5)
    assert f'/auth/user/{member.pk}/detail/' in browser.url
    assert browser.is_text_present('member', wait_time=5)
    capture(browser, 'site-search-detail')