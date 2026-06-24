import djmvc

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from . import views

User = get_user_model()


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
        views.LoginView,
        views.LogoutView,
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
            ],
        ),
    ]
