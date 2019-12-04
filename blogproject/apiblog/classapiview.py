from django.http import Http404
from rest_framework import permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from .serializers import BlogListSerializer
from webblog.models import BlogPost

from rest_framework import viewsets


class BlogList(APIView, LimitOffsetPagination):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
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
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = BlogListSerializer(blog)
        return Response(serializer.data)


class AllBlogViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = BlogPost.objects.filter(is_published=True)
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = BlogListSerializer

