"""function based views for post_list and post_details"""

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from webblog.models import BlogPost
from .serializers import BlogPostSerializer


@csrf_exempt
def api_post_list(request):
    """api for create and list the blog"""
    if request.method == 'GET':
        posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BlogPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def api_post_details(request, pk):
    """api for retrieve , update and delete"""
    try:
        posts = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = BlogPostSerializer(posts)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = BlogPostSerializer(posts, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        posts.delete()
        return HttpResponse(status=204)


@csrf_exempt
def fun_details(request, username):
    """display the name whatever used in the url"""

    if request.method == "GET":
        data = ("hi {0}".format(username))
        return JsonResponse(data, safe=False)
