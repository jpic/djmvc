import djmvc


def test_get_context_data():
    view = djmvc.generic.TemplateView()
    assert view.get_context_data()['view'] is view


def test_get_template_names():
    assert djmvc.site.routes['auth'].routes['login'].get_template_names() == [
        'djmvc/site/auth/login.html',
        'djmvc/auth/login.html',
        'djmvc/login.html',
        'djmvc/form.html',
        'site/auth/login.html',
        'auth/login.html',
        'login.html',
        'form.html',
    ]
