from rest_framework import permissions
from django.db.models import Q
from .models import Task, Employe

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class AppendedToTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if Task.objects.get(Q(user_id=request.user.id) | Q(responsible_id=request.user.id)):
            return True

class IsResponsible(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if Employe.objects.get(user_id=request.user.id, is_responsible=True):
            return True