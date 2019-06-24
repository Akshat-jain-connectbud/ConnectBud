"""NewConnectBud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from .views import login ,register_user,facebook_login,google_login
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='ConnectBud API')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', login),
    path(r'api/signup', register_user),
    path(r'api/facebook_login', facebook_login),
    path(r'api/google_login', google_login),

    path(r'$', schema_view)
]