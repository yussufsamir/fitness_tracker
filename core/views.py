from django.shortcuts import render
from rest_framework import viewsets, filters

from .permissions import IsCommentOwnerOrCoach , IsCoach
from .serializers import *
from rest_framework import generics
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView



# Create your views here.
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = Training_session.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user= self.request.user
        if not user.is_authenticated:
            return Training_session.objects.none()

        if user.is_coach:
            return Training_session.objects.filter(coach=user)
        elif user.is_client:
            return Training_session.objects.filter(assigned_clients=user)
        return Training_session.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_coach:
            raise PermissionDenied("Only coaches can create training sessions.")
        serializer.save(coach=self.request.user)
class CommentSectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsCommentOwnerOrCoach]
    queryset = CommentSection.objects.all()
    serializer_class = CommentSectionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_coach:
                
                return CommentSection.objects.filter(training_session__coach=user)
            elif user.is_client:
                
                return CommentSection.objects.filter(client=user)
        return CommentSection.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class TrainingPlanViewSet(viewsets.ModelViewSet):
    queryset = Training_plan.objects.all()
    serializer_class = TrainingPlanSerializer
    permission_classes = [IsAuthenticated, IsCoach]

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated, IsCoach]
class PlanAssignmentViewSet(viewsets.ModelViewSet):
    queryset = Plan_assignment.objects.all()
    serializer_class = PlanAssignmentSerializer
    permission_classes = [IsAuthenticated, IsCoach]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date', 'duration', 'calories_burned']
    ordering = ['-date'] 
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Activity.objects.none()

        queryset = Activity.objects.filter(user=user)

        activity_type = self.request.query_params.get('activity_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if activity_type:
            queryset = queryset.filter(activity_type__iexact=activity_type)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You cannot modify someone else's activity.")
        serializer.save()
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You cannot delete someone else's activity.")
        instance.delete()

class ActivitySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("ActivitySummaryView HIT!")
        user=self.request.user
        queryset = Activity.objects.filter(user=user)
        

        total_duration = queryset.aggregate(Sum('duration'))['duration__sum'] or 0
        total_distance = queryset.aggregate(Sum('distance'))['distance__sum'] or 0
        total_calories = queryset.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0


        return Response({
            'total_duration_minutes': total_duration,
            'total_distance': total_distance,
            'total_calories_burned': total_calories,
        })