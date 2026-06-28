"""Browser integration tests for toast notifications."""
import time

import pytest


def _wait_for_toast_absent(browser, text, timeout=6):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not browser.is_text_present(text, wait_time=0):
            return
        time.sleep(0.1)
    raise AssertionError(f'Toast still present after {timeout}s: {text!r}')


@pytest.mark.splinter(screenshot_dir='./screenshots')
@pytest.mark.django_db
def test_create_success_toast_in_browser(browser, live_server, browser_login, admin_user):
    browser_login()
    browser.visit(f'{live_server.url}/item/')

    browser.find_by_css('a[href$="/item/create/"]').first.click()
    assert browser.is_element_present_by_css('form[method="post"]', wait_time=5)

    browser.fill('name', 'BrowserAlice')
    browser.find_by_css('form[method="post"] button[type="submit"]').first.click()

    assert browser.is_text_present('was added successfully', wait_time=5)
    assert browser.is_text_present('BrowserAlice', wait_time=2)
    assert browser.is_element_present_by_css('[up-flashes] .djmvc-toast.is-success', wait_time=2)


@pytest.mark.splinter(screenshot_dir='./screenshots')
@pytest.mark.django_db
def test_create_invalid_toast_lists_field_names(browser, live_server, browser_login, admin_user):
    browser_login()
    browser.visit(f'{live_server.url}/item/')

    browser.find_by_css('a[href$="/item/create/"]').first.click()
    assert browser.is_element_present_by_css('form[method="post"]', wait_time=5)

    browser.driver.execute_script(
        "document.querySelector('#id_name').removeAttribute('required')"
    )
    browser.fill('name', '')
    browser.find_by_css('form[method="post"] button[type="submit"]').first.click()

    assert browser.is_text_present('Please correct the error below', wait_time=5)
    assert browser.is_element_present_by_css('[up-flashes] .djmvc-toast.is-danger', wait_time=2)


@pytest.mark.splinter(screenshot_dir='./screenshots')
@pytest.mark.django_db
def test_toast_dismiss_button(browser, live_server, browser_login, admin_user):
    browser_login()
    browser.visit(f'{live_server.url}/item/')

    browser.find_by_css('a[href$="/item/create/"]').first.click()
    assert browser.is_element_present_by_css('form[method="post"]', wait_time=5)

    browser.fill('name', 'DismissMe')
    browser.find_by_css('form[method="post"] button[type="submit"]').first.click()

    assert browser.is_text_present('DismissMe', wait_time=5)
    browser.find_by_css('[up-flashes] .djmvc-toast .delete').first.click()
    _wait_for_toast_absent(browser, 'DismissMe', timeout=3)


@pytest.mark.splinter(screenshot_dir='./screenshots')
@pytest.mark.django_db
def test_toast_auto_dismiss(browser, live_server, browser_login, admin_user):
    browser_login()
    browser.visit(f'{live_server.url}/item/')

    browser.find_by_css('a[href$="/item/create/"]').first.click()
    assert browser.is_element_present_by_css('form[method="post"]', wait_time=5)

    browser.fill('name', 'AutoDismiss')
    browser.find_by_css('form[method="post"] button[type="submit"]').first.click()

    assert browser.is_text_present('AutoDismiss', wait_time=5)
    _wait_for_toast_absent(browser, 'AutoDismiss', timeout=6)