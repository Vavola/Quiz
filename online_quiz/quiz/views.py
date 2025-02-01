from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Quiz
from .forms import QuizForm
from django.contrib.auth.views import LoginView, LogoutView
@login_required
def dashboard(request):
    quizzes = Quiz.objects.filter(created_by=request.user)
    return render(request, 'quiz/dashboard.html', {'quizzes': quizzes})

class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/quiz_list.html'
    context_object_name = 'quizzes'

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['title', 'description']
    template_name = 'quiz/quiz_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'

def profile(request):
    return render(request, 'accounts/profile.html')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'accounts/logout.html'