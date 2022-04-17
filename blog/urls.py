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
from django.urls import path,include,re_path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('news/',views.news),
    path('login/',views.login),
    path('sign/',views.sign),
    path("login/random_code/",views.get_random_code),
    path("Led/",views.mqtt),
    path("Led/<int:pin>",views.mqtt_led),
    path("logout/",views.logout),
    #路由分发，将所有api开头的分发到api下的urls
    re_path(r'^api/',include('api.urls')),
    re_path(r'^article/(?P<nid>\d+)/',views.article)
]
