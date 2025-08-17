from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'training-sessions', TrainingSessionViewSet)
router.register(r'comments', CommentSectionViewSet)
router.register(r'training-plans', TrainingPlanViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'plan-assignments', PlanAssignmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
