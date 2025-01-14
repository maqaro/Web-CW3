"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from .views import main_spa, register_view, login_view, profile_view, get_users, logout_view

urlpatterns = [
    path('api/register/', register_view, name='register'),
    path('api/login/', login_view, name='login'),
    path('api/users-hobbies/', get_users, name='users-hobbies'),
    path('profile', profile_view, name='profile'),
    path('api/logout/', logout_view, name='logout'),
    path('', main_spa, name='main_spa'),
]
