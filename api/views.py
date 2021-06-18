from django_filters.utils import verbose_field_name
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from .permissions import IsOwnerOrReadOnly, AppendedToTask, IsResponsible
from .models import Responsible, Task, Comment
from django.contrib.auth.models import AbstractUser, User

from django.core import serializers as core_serializers


from rest_framework.authtoken.views import ObtainAuthToken

class ObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class TasksViewList(generics.ListAPIView):
    serializer_class = Task
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['priority', 'status']
    search_filter = ['task_name']

    def get(self, request):
        userID = int(request.data['user_id'])
        usr = User.objects.get(pk=userID)
        employe = usr.employe

        if employe.is_responsible == False:
            data = core_serializers.serialize('json', Task.objects.filter(user_id=employe.id).order_by('priority__priority'))
            return Response(data)
        if employe.is_responsible == True:
            data = core_serializers.serialize('json', Task.objects.filter(responsible_id=employe.id).order_by('priority__priority'))
            return Response(data)

class TaskDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = Task
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request):
        task_id = int(request.data['task_id'])

        data = core_serializers.serialize('json', Task.objects.get(pk=task_id))
        return Response(data)

class CommentsViewList(generics.ListAPIView):
    serializer_class = Comment
    permission_classes = [IsAuthenticated]

    def get(self, request):
        taskID = int(request.data['task_id'])
        data = core_serializers.serialize('json', Comment.objects.filter(task_id=taskID).order_by('date'))

        return Response(data)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = Comment
    permission_classes = (AppendedToTask,)
