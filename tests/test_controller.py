from django.contrib.auth.models import AnonymousUser

from djmvc.controller import Controller
from djmvc.view import View


def test_get_tagged_views(rf, admin_user):
    class LoginView(View):
        tags = ['topbar']

        def has_permission(self):
            return not self.request.user.is_authenticated

    class LogoutView(View):
        tags = ['topbar']

        def has_permission(self):
            return self.request.user.is_authenticated

    class Site(Controller):
        routes = [
            LoginView,
            Controller.clone(routes=[LogoutView]),
        ]

    site = Site()
    site.build()
    request = rf.get('/')
    request.user = AnonymousUser()
    result = site.get_tagged_views('topbar', request=request)
    assert len(result) == 1
    assert type(result[0]).__name__ == 'LoginView'
    assert result[0].request is request

    request.user = admin_user
    result = site.get_tagged_views('topbar', request=request)
    assert len(result) == 1
    assert type(result[0]).__name__ == 'LogoutView'


def test_registry():
    from djmvc.registry import Registry

    class MyController(Controller):
        routes = [View]

    controller = MyController()
    controller.build()
    assert isinstance(controller.routes, Registry)
    assert not hasattr(View, 'controller')
