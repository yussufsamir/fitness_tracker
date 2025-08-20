from rest_framework import serializers
from .models import Activity, Training_session, CommentSection, Exercise, Session_exercise,User,Training_plan,Plan_assignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_coach', 'is_client']
        read_only_fields = ['id', 'username', 'is_coach', 'is_client']

class TrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_session
        fields = ['id', 'coach', 'date', 'duration', 'title', 'description', 'assigned_clients','activity_type','distance_km','calories_burned']
        read_only_fields = ['id', 'created_at', 'updated_at','coach']

class CommentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentSection
        fields = ['id', 'training_session', 'client', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at','client']

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

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_coach', 'is_client']

    def validate(self, data):
        if data.get('is_coach') and data.get('is_client'):
            raise serializers.ValidationError("A user cannot be both a coach and a client.")
        if not data.get('is_coach') and not data.get('is_client'):
            raise serializers.ValidationError("User must be either a coach or a client.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            is_coach=validated_data['is_coach'],
            is_client=validated_data['is_client']
        )
        return user

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date']
        read_only_fields = ['id', 'user', 'date']