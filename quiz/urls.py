from django.urls import path
from . import views
from .views import play_quiz

urlpatterns = [
    path('', views.QuizListView.as_view(), name='quiz_list'),
    path('create/', views.create_quiz, name='quiz_create'),
    path('<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:quiz_id>/play/', play_quiz, name='play_quiz'),
    path('<int:pk>/submit/', views.submit_quiz, name='submit_quiz'),
]



