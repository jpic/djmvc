import functools

from django.views import generic

from djmvc.view import ViewMixin
from djmvc_example.models import User


def test_view_security(rf, admin_user):
    class UserDetailView(ViewMixin, generic.DetailView):
        queryset = User.objects.all()

        def has_permission(self):
            return self.request.user == self.object

        @functools.cached_property
        def object(self):
            return self.get_object()

    request = rf.get('/')
    UserDetailView(request=request, object=admin_user)