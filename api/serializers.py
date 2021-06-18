from django.db.models import fields
from rest_framework import serializers
from .models import Comment, Employe, Task
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TaskSerializer(serializers.ModelSerializer):
    many = True
    class Meta:
        model = Task
        fields = ['name']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


