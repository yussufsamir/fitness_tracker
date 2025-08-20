# core/permissions.py
from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsCommentOwnerOrCoach(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.client == user:
            return True

        
        if obj.training_session.coach == user:
            return True

        
        return False
    
class IsCoach(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_coach', False)
