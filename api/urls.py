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
from api.views import login, article, comment, user, file, api_email, sites

urlpatterns = [
    path('login/', login.LoginView.as_view()),
    path('sign/', login.SignView.as_view()),
    path('article/', article.ArticleView.as_view()),
    re_path(r'article/(?P<nid>\d+)/', article.ArticleView.as_view()),
    re_path(r'article/comment/(?P<nid>\d+)/', comment.CommentView.as_view()),
    re_path(r'comment/digg/(?P<nid>\d+)/', comment.CommentDiggView.as_view()),
    re_path(r'article/digg/(?P<nid>\d+)/', article.ArticleDiggView.as_view()),
    re_path(r'article/collects/(?P<nid>\d+)/', article.ArticleCollectsView.as_view()),
    path('edit_password/', user.EditPasswordView.as_view()),
    path('edit_avatar/', user.EditAvatarView.as_view()),
    path('upload/avatar/', file.AvatarView.as_view()),
    re_path(r'delete/avatar/(?P<nid>\d+)/', file.AvatarView.as_view()),
    path('upload/cover/', file.CoverView.as_view()),
    re_path(r'delete/cover/(?P<nid>\d+)/', file.CoverView.as_view()),
    path('send_email/', api_email.ApiEmail.as_view()),
    path('perfect_information/', user.EditUserInfoView.as_view()),
    path('cancel_collection/', user.CancelCollectionView.as_view()),
    path('site_tag/', sites.NavTagsView.as_view()),
    re_path(r'site_tag/(?P<nid>\d+)/', sites.NavTagsView.as_view()),
    path('sites/', sites.NavView.as_view()),
    re_path(r'sites/(?P<nid>\d+)/', sites.NavView.as_view()),
    re_path(r'site_digg/(?P<nid>\d+)/', sites.NavDiggView.as_view()),
    re_path(r'site_coll/(?P<nid>\d+)/', sites.NavCollectsView.as_view()),
    path('friends_links/', sites.FriendLinksView.as_view()),
    path('feedback/', user.FeedBackView.as_view()),
    re_path(r'article/cover/(?P<nid>\d+)/', article.EditArticleCoverView.as_view()),
]