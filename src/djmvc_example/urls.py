"""
URL configuration for djmvc_example project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

import djmvc
from djmvc_auth.controller import AuthController

class Site(djmvc.Controller):
    name = 'Example project'
    urlpath = ''
    routes = [
        djmvc.generic.TemplateView.clone(
            icon='home',
            template_name='home.html',
            name='Home',
            menus=['topbar'],
            urlname='home',
            urlpath='',
            has_permission=lambda view: True,  # allow non-authenticated
        ),
        AuthController,
    ]

site = Site()

urlpatterns = [
    path("admin/", admin.site.urls),
] + site.urlpatterns
