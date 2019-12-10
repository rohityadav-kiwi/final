"""class based api views"""
from django.http import Http404
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from webblog.models import BlogPost
from .serializers import BlogListSerializer


class BlogList(APIView, LimitOffsetPagination):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        """get mehtod to get list of posts with pagination"""
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        queryset = BlogPost.objects.all()
        page = paginator.paginate_queryset(queryset, request)
        serializer = BlogListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class BlogDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self, pk):
        """trying to get the blog with particular pk"""
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """retrieve, update , delete blog with pk given """
        blog = self.get_object(pk)
        serializer = BlogListSerializer(blog)
        return Response(serializer.data)


class AllBlogViewSet(viewsets.ReadOnlyModelViewSet):
    """ReadOnlyModelViewSet used to only retrieve and list the blog"""

    queryset = BlogPost.objects.filter(is_published=True)
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = BlogListSerializer
