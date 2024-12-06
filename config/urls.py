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
from django.conf import settings
from django.conf.urls.static import static as thisstatic
from profiles.views import *
from kanban.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__reload__/", include("django_browser_reload.urls")),

    path('', TemplateView.as_view(template_name='homepage.html'), name='home'),
    path('loginDirect', TemplateView.as_view(template_name='loadLogin.html'), name='login_success'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', TemplateView.as_view(template_name='registration/logout.html'), name='account_logout'),
    path('profile/', profile_view, name='profile'),
    path('<username>/', profile_view, name='user_profile'),
    path('profile/my-profile/', profile_detail_view, name='profile_detail'),
    path('profile/my-profile/detail_edit/', profile_detail_edit_view, name='profile_detail_edit'),
    path('profile/my-profile/bio_edit/', profile_bio_edit_view, name='profile_bio_edit'),
    path('profile/my-profile/picture_edit/', profile_picture_edit_view, name='profile_picture_edit'),
    path('profile/my-profile/deactivate/', profile_deactivate, name='profile_deactivate'),
    path('profile/my-kanban/', profile_kanban_view, name='profile_kanban'),
    path('profile/my-account/', profile_account_view, name='profile_account'),
    path('profile/my-report/', profile_report_view, name='profile_report'),

]
if settings.DEBUG:
    urlpatterns += thisstatic(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)