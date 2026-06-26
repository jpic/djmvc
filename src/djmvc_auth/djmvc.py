import djmvc
from django.conf import settings
from django.urls import reverse_lazy

from .views import AuthController

djmvc.site.routes.register(AuthController)
settings.LOGIN_URL = reverse_lazy('site:auth:login')