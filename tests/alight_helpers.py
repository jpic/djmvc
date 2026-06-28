import time

INPUT_SELECTOR = 'autocomplete-select-input input'
DROPDOWN_SELECTOR = '.autocomplete-light-box'
OPTION_SELECTOR = '.autocomplete-light-box [data-value]:not([data-create])'


def wait_alight_ready(browser, timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if browser.evaluate_script(
                "customElements.get('autocomplete-select') !== undefined"
                " && !document.querySelector("
                "'autocomplete-select-input:not([data-bound]),"
                " autocomplete-select:not([data-bound])')"
            ):
                return
        except Exception:
            pass
        time.sleep(0.15)
    raise AssertionError('autocomplete-select was not ready')


def open_autocomplete(browser, input_css=INPUT_SELECTOR):
    browser.execute_script(
        """
        var el = document.querySelector(arguments[0]);
        if (el && document.activeElement === el) { el.blur(); }
        """,
        input_css,
    )
    browser.find_by_css(input_css).first.click()


def type_and_select(browser, text, *, container_css='autocomplete-select', input_css=None):
    if input_css is None:
        input_css = f'{container_css} {INPUT_SELECTOR}'
    wait_alight_ready(browser)
    open_autocomplete(browser, input_css)
    field = browser.find_by_css(input_css).first
    field.value = ''
    field.type(text)

    deadline = time.time() + 5
    while time.time() < deadline:
        if browser.is_element_present_by_css(OPTION_SELECTOR, wait_time=0):
            for option in browser.find_by_css(OPTION_SELECTOR):
                if text in option.text:
                    option.click()
                    return
        time.sleep(0.15)
    raise AssertionError(f'No autocomplete option matching {text!r}')


def selected_labels(browser, container_css='autocomplete-select'):
    selector = f'{container_css} [slot=deck] [data-value]'
    return [
        el.text.replace('×', '').strip()
        for el in browser.find_by_css(selector)
    ]