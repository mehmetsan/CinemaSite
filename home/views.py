from django.shortcuts import render, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def landing_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    else:
        return render(request, template_name="landing.html", context={})


def home_view(request):
    if request.user.is_authenticated:
        return render(request, template_name="home.html", context={})
    else:
        return HttpResponseRedirect('/')


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login( request, user)
        return HttpResponseRedirect('/')

    return render(request, template_name="login.html", context={'form': form})


def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()

        user = authenticate(username=username, password=password)
        login(request, user)
        return render(request, template_name="home.html", context={})

    return render(request, template_name="register.html", context={'form': form})


def logout_view(request):
    logout(request)
    return render(request, template_name="landing.html", context={})