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
from django.urls import path, re_path
from api.views import login, article, comment

urlpatterns = [
    path('login/', login.LoginView.as_view()),
    path('sign/', login.SignView.as_view()),
    path('article/', article.ArticleView.as_view()),
    re_path(r'article/(?P<nid>\d+)/', article.ArticleView.as_view()),
    re_path(r'article/comment/(?P<nid>\d+)', comment.CommentView.as_view()),
]