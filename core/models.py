from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractUser):
    is_coach= models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Training_plan(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_coach': True})
    title=models.TextField()
    goal=models.TextField()
    description=models.TextField(blank=True, null=True)
    start_date=models.DateField()
    end_date=models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date", "-id"]
        indexes = [models.Index(fields=["coach", "start_date"])]

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("end_date cannot be before start_date.")

    def __str__(self):
        return self.title


class Plan_assignment(models.Model):
    training_plan = models.ForeignKey(Training_plan, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_client': True})
    status = models.CharField(
        max_length=20,
        choices=[("assigned", "Assigned"), ("active", "Active"), ("completed", "Completed"), ("archived", "Archived")],
        default="assigned",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("training_plan", "client")
        indexes = [models.Index(fields=["training_plan", "client"])]

    def __str__(self):
        return f"{self.client} ↔ {self.training_plan} ({self.status})"

class Training_session(models.Model):
    training_plan = models.ForeignKey(
        Training_plan, on_delete=models.SET_NULL, related_name="sessions", null=True, blank=True
    )
    coach = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_coach': True})
    date = models.DateField()
    duration = models.DurationField(help_text="HH:MM:SS (e.g., 01:30:00 for 90 minutes)")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    assigned_clients = models.ManyToManyField(User, related_name='training_sessions', limit_choices_to={'is_client': True},blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ACTIVITY_CHOICES = [
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Weightlifting', 'Weightlifting'),
        ('Swimming', 'Swimming'),
        ('Walking', 'Walking'),
        ('Yoga', 'Yoga'),
    ]
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES,default='Running')
    distance_km = models.FloatField(blank=True, null=True)
    calories_burned = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["-date", "-id"]
        indexes = [models.Index(fields=["coach", "date"])]

    def clean(self):
        if self.duration is not None and self.duration <= timedelta(0):
            raise ValidationError("duration must be positive.")
        if self.training_plan:
            if not (self.training_plan.start_date <= self.date <= self.training_plan.end_date):
                raise ValidationError("session date must be within the plan's date range.")
            if self.training_plan.coach_id != self.coach_id:
                raise ValidationError("session coach must match the plan's coach.")

    def __str__(self):
        return f"{self.title} ({self.date})"
    

class CommentSection(models.Model):
    training_session = models.ForeignKey(Training_session, on_delete=models.CASCADE, related_name='comments')
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_client': True})
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["training_session", "created_at"])]

    def clean(self):
        # Only clients assigned to the session can comment
        if not self.training_session.assigned_clients.filter(pk=self.client_id).exists():
            raise ValidationError("Client must be assigned to this session to comment.")

    def __str__(self):
        return f"{self.client.username} - {self.comment[:20]}..."
class Exercise(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Session_exercise(models.Model):
    training_session=models.ForeignKey(Training_session, on_delete=models.CASCADE, related_name='session_exercises')
    exercise=models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='session_exercises')
    order = models.PositiveSmallIntegerField(default=1)
    sets = models.PositiveSmallIntegerField(null=True, blank=True)
    reps = models.PositiveSmallIntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duration_sec = models.PositiveIntegerField(null=True, blank=True)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rest_sec = models.PositiveIntegerField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["training_session", "order", "id"]      
        unique_together = ("training_session", "order")     
        indexes = [models.Index(fields=["training_session", "order"])]

    def __str__(self):
        core = []
        if self.sets: core.append(f"{self.sets}x")
        if self.reps: core.append(f"{self.reps}")
        main = " ".join(core) or "prescription"
        return f"{self.exercise.name} – {main}"
    
class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Weightlifting', 'Weightlifting'),
        ('Swimming', 'Swimming'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    distance = models.FloatField(null=True, blank=True)
    calories_burned = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"



