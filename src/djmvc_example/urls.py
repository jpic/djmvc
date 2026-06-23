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

from djmvc.controller import Controller
from djmvc_auth.crud import AuthController

site = Controller.clone(
    name='Example project',
)(
    views=[
        TemplateView.clone(
            icon='home',
            template_name='djmvc/home.html',
            title='djmvc',
            title_heading='Welcome to djmvc',
            menus=['main'],
            urlname='home',
            urlpath='',
            has_perm=True,  # allow non-authenticated
        ),
        AuthController,
    ]
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', site().urlpatterns, namespace='site'),
]
