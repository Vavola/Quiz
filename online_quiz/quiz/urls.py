from django.urls import path
from .views import QuizListView, QuizCreateView, QuizDetailView, dashboard

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('create/', QuizCreateView.as_view(), name='quiz_create'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('dashboard/', dashboard, name='dashboard'),
]