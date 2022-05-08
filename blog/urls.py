"""blog URL Configuration

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
from django.contrib import admin
from django.urls import path, include, re_path
from app01.views import index, backend
from django.conf import settings 
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_home/', backend.admin_home),
    path('', index.index),
    path('news/', index.news),
    path('about/', index.about),
    path('history/', index.history),
    path('sites/', index.sites),
    path('moods/', index.moods),

    path('search/', index.search),
    path('login/', index.login),
    path('sign/', index.sign),
    path("login/random_code/", index.get_random_code),
    path("Led/", index.mqtt),
    path("Led/<int:pin>", index.mqtt_led),
    path("logout/", index.logout),
    path("backend/", backend.backend),
    path("backend/add_article/", backend.add_article),
    path("backend/edit_avatar/", backend.edit_avatar),
    path("backend/reset_password/", backend.reset_password),
    path('backend/avatar_list/', backend.avatar_list),
    path('backend/cover_list/', backend.cover_list),
    # 路由分发，将所有api开头的分发到api下的urls
    re_path(r'^api/', include('api.urls')),
    re_path(r'^article/(?P<nid>\d+)/', index.article),
    re_path(r'^backend/edit_article/(?P<nid>\d+)/', backend.edit_article),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
