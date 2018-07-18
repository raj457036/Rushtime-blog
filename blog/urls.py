"""blog URL Configuration

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
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from post import views as post_view
from registration import views as r_view, forms as reg_form
from .views import HomeView, search_result_sync, follow_user

urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('login/', r_view.RegLogin.as_view(),name='user_login'),
    path('signup/', r_view.signup, name='user_signup'),
    path('logout/', r_view.RegLogout.as_view(), name='user_logout'),
    path('user/', include('registration.urls')),
    path('notices/', include('notifiy.urls')),

    # apis
    path('api/search', search_result_sync, name='api_search'),
    path('api/follow', follow_user, name='api_follow')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)