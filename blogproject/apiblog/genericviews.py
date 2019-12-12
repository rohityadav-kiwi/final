from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer,  MyBlogSerializer
from rest_framework import generics, status, permissions, viewsets
from webblog.models import BlogPost


class GenericBlogCreate(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def create(self, request, *args, **kwargs):
        kwargs.update({'request': request})
        serializer = BlogPostSerializer(data=request.data, context=kwargs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': "error message"}, status=status.HTTP_400_BAD_REQUEST)


class GenericMyBlogList(generics.ListAPIView):
    serializer_class = MyBlogSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return BlogPost.objects.filter(author=user)


class GenericBlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class MyBlogViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def create(self, request, *args, **kwargs):
        kwargs.update({'request': request})
        serializer = BlogPostSerializer(data=request.data, context=kwargs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': "error message"}, status=status.HTTP_400_BAD_REQUEST)
    