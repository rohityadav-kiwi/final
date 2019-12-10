""" django urls are checked here"""
from rest_framework import routers
from django.urls import path, include
from .classapiview import BlogList, BlogDetail, AllBlogViewSet
from .accounts import signup, login
from .views import api_post_list, api_post_details, fun_details
from .genericviews import GenericBlogCreate, GenericMyBlogList, GenericBlogDetail, MyBlogViewSet


router = routers.SimpleRouter()

urlpatterns = [
    path("myblogs/", GenericMyBlogList.as_view(), name="api_my_blog"),
    path("create/", GenericBlogCreate.as_view(), name="api_create_blog"),
    path("myblogs/<int:pk>/", GenericBlogDetail.as_view(), name="api_update_delete"),
    path("blog/", BlogList.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetail.as_view(), name='blog_detail'),
    path("posts/", api_post_list, name='api_post_list'),
    path('posts/<int:pk>/', api_post_details, name='api_post-detail'),
    path('signup/', signup, name='SignupView'),
    path('login/', login, name='loginView'),
    path('fun/<username>/', fun_details, name="just_fun"),
]

router.register('blogs', AllBlogViewSet)
router.register('my-blogs', MyBlogViewSet)

urlpatterns += [
    path('', include(router.urls)),
]
