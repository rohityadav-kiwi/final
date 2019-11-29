""" django urls are checked here"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .classapiview import BlogList, BlogDetail
from .accounts import signup, login
from .views import post_list, post_details

urlpatterns = [
    path("blog/", BlogList.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetail.as_view(), name='blog_detail'),
    path("posts/", post_list, name='post_list'),
    path('posts/<int:pk>/', post_details, name='post-detail'),
    path('signup/', signup, name='SignupView'),
    path('login/', login, name='loginView'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
