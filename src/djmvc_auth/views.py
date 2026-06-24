import djmvc
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


class LoginView(djmvc.generic.FormView):
    form_class = AuthenticationForm
    tags = ['topbar', 'navigation']
    icon = 'box-arrow-in-right'
    form_attributes = {
        'up-target': 'body',
        'up-history': 'false',
    }

    def has_permission(self):
        """ Show login only to anonymous users. """
        return not self.request.user.is_authenticated

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(djmvc.generic.FormView):
    tags = ['topbar', 'navigation']
    icon = 'box-arrow-right'
    message = 'Are you sure you want to logout ?'
    form_attributes = {
        'up-target': 'body',
        'up-history': 'false',
    }
    action = 'click->modal#open'

    def has_permission(self):
        """ Show login only to authenticated users. """
        return self.request.user.is_authenticated

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)
