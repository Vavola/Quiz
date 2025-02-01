from django.shortcuts import render, redirect
from accounts.forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView

def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'
    http_method_names = ['get', 'post']


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})