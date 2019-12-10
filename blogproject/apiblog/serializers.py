"""Serializers is used to convert query_sets and model
    instances to native Python data types that
    can then be easily rendered into JSON. it also can be used for data validation"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from webblog.models import Profile, BlogPost


class UserSerializer(serializers.ModelSerializer):
    """serializer for the signup"""

    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())]
                                   )
    username = serializers.CharField(max_length=32, required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all())]
                                     )
    password = serializers.CharField(required=True, min_length=8, write_only=True)

    def create(self, validated_data):
        """overriding the predefined django create method to give token to the
            new user"""

        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])
        Token.objects.create(user=user)
        return user

    class Meta:
        """fields and model to use"""
        model = Profile
        fields = ('id', 'username', 'email', 'password')


class BlogPostSerializer(serializers.ModelSerializer):
    """blog_post_serializer is used for creating the blog """
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """fields and model to use"""
        model = BlogPost
        fields = ['id', 'title', 'author', 'post_content', 'is_published']


class BlogListSerializer(serializers.ModelSerializer):
    """this serializer is used to list all the blog"""
    author = serializers.SerializerMethodField()

    @staticmethod
    def get_author(obj):
        """overriding to get the author name"""
        if obj.author:
            return obj.author.username
        return None

    class Meta:
        """fields and model to use"""
        model = BlogPost
        fields = ['id', 'title', 'author', 'post_content', 'is_published']


class LoginSerializer(serializers.ModelSerializer):
    """login serializer to validate the user"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        """fields and model to use"""
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        """validate the username and password"""
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("User doesn't exist or invalid password ")
        return attrs


class MyBlogSerializer(serializers.ModelSerializer):
    """my blog serializer for showing only logged in user blog"""

    class Meta:
        """fields and model to use"""
        model = BlogPost
        fields = ['id', 'title', 'post_content', 'is_published']
