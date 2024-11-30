"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import TemplateView
from profiles.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__reload__/", include("django_browser_reload.urls")),

    path('', TemplateView.as_view(template_name='homepage.html'), name='home'),
    path('logout/', TemplateView.as_view(template_name='registration/logout.html'), name='account_logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/my-profile/', profile_detail_view, name='profile_detail'),
    path('profile/my-kanban/', profile_kanban_view, name='profile_kanban'),
    path('profile/my-account/', profile_account_view, name='profile_account'),
    path('profile/my-report/', profile_report_view, name='profile_report'),

]
