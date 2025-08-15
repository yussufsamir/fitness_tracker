from rest_framework import serializers
from .models import Training_session, CommentSection, Exercise, Session_exercise,User,Training_plan,Plan_assignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_coach', 'is_client']

class TrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_session
        fields = ['id', 'coach', 'date', 'duration', 'title', 'description', 'assigned_clients']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CommentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentSection
        fields = ['id', 'training_session', 'client', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

class TrainingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_plan
        fields = ['id', 'coach', 'title', 'goal', 'description', 'start_date', 'end_date']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SessionExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session_exercise
        fields = ['id', 'training_session', 'exercise', 'order', 'sets', 'reps', 'weight_kg', 'duration_sec', 'distance_km', 'rest_sec', 'notes']
        read_only_fields = ['id']

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class PlanAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan_assignment
        fields = ['id', 'training_plan', 'client', 'assigned_at']
        read_only_fields = ['id', 'assigned_at']