from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'training-sessions', TrainingSessionViewSet)
router.register(r'comments', CommentSectionViewSet)
router.register(r'training-plans', TrainingPlanViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'plan-assignments', PlanAssignmentViewSet)
router.register(r'activities', ActivityViewSet, basename='activity')



urlpatterns = [
    path('activities/summary/', ActivitySummaryView.as_view(), name='activity-summary'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
    
    
]
