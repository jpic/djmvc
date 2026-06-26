import djmvc
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)


User = get_user_model()


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


def get_custom_user_creation_form():
    """Return UserCreationForm for the configured AUTH_USER_MODEL.

    Django's default forms are hardcoded to auth.User, so we create
    a new form class with type() that uses settings.AUTH_USER_MODEL instead.
    """
    return type(
        'CustomUserCreationForm',
        (UserCreationForm,),
        {'Meta': type('Meta', (), {'model': User, 'fields': UserCreationForm.Meta.fields})}
    )


def get_custom_user_change_form():
    """Return UserChangeForm for the configured AUTH_USER_MODEL.

    Django's default forms are hardcoded to auth.User, so we create
    a new form class with type() that uses settings.AUTH_USER_MODEL instead.
    """
    return type(
        'CustomUserChangeForm',
        (UserChangeForm,),
        {'Meta': type('Meta', (), {'model': User, 'fields': '__all__'})}
    )


class AuthController(djmvc.Controller):
    routes = [
        LoginView,
        LogoutView,
        djmvc.ModelController.clone(
            model=User,
            routes=[
                djmvc.generic.ListView.clone(
                    table_fields=[
                        'id',
                        'username',
                        'email',
                        'is_active',
                        'actions',
                    ],
                    icon='person',
                ),
                djmvc.generic.DetailView,
                djmvc.generic.CreateView.clone(
                    form_class=get_custom_user_creation_form(),
                ),
                djmvc.generic.UpdateView.clone(
                    form_class=get_custom_user_change_form(),
                ),
                djmvc.generic.DeleteView,
                djmvc.generic.DeleteObjectsView,
            ],
        ),
    ]
