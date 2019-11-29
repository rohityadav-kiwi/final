from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import UserSerializer, LoginSerializer


@api_view(http_method_names=['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            username = data.get('username')
            user = User.objects.get(username=username)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},
                            status=HTTP_200_OK)
        return Response(serializer.errors, status=400)


@api_view(http_method_names=['POST'])
def signup(request):
    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)