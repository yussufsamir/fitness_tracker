from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from rest_framework import generics
# Create your views here.
class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = Training_session.objects.all()
    serializer_class = TrainingSessionSerializer

    def get_queryset(self):
        user= self.request.user
        if user.is_coach:
            return Training_session.objects.filter(coach=user)
        elif user.is_client:
            return Training_session.objects.filter(assigned_clients=user)
        return Training_session.objects.none()

    def perform_create(self, serializer):
        serializer.save(coach=self.request.user)

class CommentSectionViewSet(viewsets.ModelViewSet):
    queryset = CommentSection.objects.all()
    serializer_class = CommentSectionSerializer

class TrainingPlanViewSet(viewsets.ModelViewSet):
    queryset = Training_plan.objects.all()
    serializer_class = TrainingPlanSerializer

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class PlanAssignmentViewSet(viewsets.ModelViewSet):
    queryset = Plan_assignment.objects.all()
    serializer_class = PlanAssignmentSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer