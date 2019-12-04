""" django urls are checked here"""
from django.db import router
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .classapiview import BlogList, BlogDetail, AllBlogViewSet
from .accounts import signup, login
from .views import post_list, post_details
from .genericviews import GenericBlogCreate, GenericMyBlogList, GenericBlogDetail, MyBlogViewSet
from rest_framework import routers
from rest_framework.routers import SimpleRouter

routers = routers.SimpleRouter()


urlpatterns = [
    path("myblogs/", GenericMyBlogList.as_view(), name="api_my_blog"),
    path("create/", GenericBlogCreate.as_view(), name="api_create_blog"),
    path("myblogs/<int:pk>/", GenericBlogDetail.as_view(), name="api_update_delete"),
    path("blog/", BlogList.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetail.as_view(), name='blog_detail'),
    path("posts/", post_list, name='post_list'),
    path('posts/<int:pk>/', post_details, name='post-detail'),
    path('signup/', signup, name='SignupView'),
    path('login/', login, name='loginView'),
]

router = SimpleRouter()

router.register('blogs', AllBlogViewSet)
router.register('my-blogs', MyBlogViewSet)

urlpatterns += [
    path('', include(router.urls)),
]