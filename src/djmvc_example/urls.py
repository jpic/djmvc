from django.contrib import admin
from django.urls import path

import djmvc

urlpatterns = [
    path("admin/", admin.site.urls),
] + djmvc.site.build().urlpatterns

handler400 = "djmvc.handlers.handler400"
handler403 = "djmvc.handlers.handler403"
handler404 = "djmvc.handlers.handler404"
handler500 = "djmvc.handlers.handler500"