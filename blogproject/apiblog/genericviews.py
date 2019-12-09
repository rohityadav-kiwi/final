"""generics views used for the create , list, update, delete, Retrieve """
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from webblog.models import BlogPost
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer, MyBlogSerializer


class GenericBlogCreate(generics.CreateAPIView):
    """view for create he blog"""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def create(self, request, *args, **kwargs):
        """overriding the  create method"""
        kwargs.update({'request': request})
        serializer = BlogPostSerializer(data=request.data, context=kwargs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': "error message"}, status=status.HTTP_400_BAD_REQUEST)


class GenericMyBlogList(generics.ListAPIView):
    """view to display the list of my blog"""
    serializer_class = MyBlogSerializer

    def get_queryset(self):
        """
        This view should return a list of all the post
        for the currently authenticated user.
        """
        user = self.request.user
        return BlogPost.objects.filter(author=user)


class GenericBlogDetail(generics.RetrieveUpdateDestroyAPIView):
    """view to do retrieve, update, delete"""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class MyBlogViewSet(viewsets.ModelViewSet):
    """models_view_set can be used to do create ,update, delete, retrieve, list """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """overriding the queryset to flter post according to logged in user"""
        return self.queryset.filter(author=self.request.user)

    def create(self, request, *args, **kwargs):
        """overriding the create method"""
        kwargs.update({'request': request})
        serializer = BlogPostSerializer(data=request.data, context=kwargs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': "error message"}, status=status.HTTP_400_BAD_REQUEST)



