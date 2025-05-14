"""
URL configuration for user_skills_bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from bot import views
from django.shortcuts import render
from django.contrib.staticfiles.urls import staticfiles_urlpatterns #TODO REMOVE WHEN GOING LIVE
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('admin/', admin.site.urls),
    path('city_form/', views.city_form_view, name='city_form'),
    path('user_form/', views.user_form_view, name='user_form'),
    path('success/', lambda request: render(request, 'success'), name='success'),
    path('accounts/', include('allauth.urls')),
    path('slack/login/', RedirectView.as_view(url='/accounts/slack/login/'), name='slack_login'),
]


urlpatterns += staticfiles_urlpatterns()