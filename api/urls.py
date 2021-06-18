from django.urls import include, re_path, path
from rest_framework import routers
from rest_framework.generics import CreateAPIView
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'api'
urlpatterns = [
    path('get/tasks/', TasksViewList.as_view()),
    path('get/task/<int:pk>/', TaskDetailView.as_view()),
    # path('create/task/', TaskCreateView.as_view()),
    path('get/comments/', CommentsViewList.as_view()),
    path('create/comment/', CommentCreateView.as_view()),
    # path('create/task/', TaskCreateView.as_view()),
    path('login/', ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
