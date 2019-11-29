from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.validators import UniqueValidator
from webblog.models import Profile, BlogPost
# from .models import ApiProfile, ApiBlogPost


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())]
                                   )
    username = serializers.CharField(max_length=32, validators=[UniqueValidator(queryset=User.objects.all())]
                                     )
    password = serializers.CharField(required=True, min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])
        Token.objects.create(user=user)
        return user

    class Meta:
        model = Profile
        fields = ('id', 'username', 'email', 'password')


class BlogPostSerializer(serializers.ModelSerializer):
    pass
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'post_content', 'is_published']


class LoginSerializer(serializers.ModelSerializer):
    pass
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("User doesn't exist or invalid password ")
        return attrs
