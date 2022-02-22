from django.shortcuts import render, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout


# Displays the main landing page for user actions
def landing_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    else:
        return render(request, template_name="landing.html", context={})


# Displays the home page if the user is logged in
# Else redirects to the landing page
def home_view(request):
    if request.user.is_authenticated:
        return render(request, template_name="home.html", context={})
    else:
        return HttpResponseRedirect('/')


# Displays the login page for an unauthorized user
# Else redirects to the home page
def login_view(request):
    if not request.user.is_authenticated:
        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            login( request, user)
            return HttpResponseRedirect('/')

        return render(request, template_name="login.html", context={'form': form})
    return HttpResponseRedirect('/home')


# Displays the register page for an unauthorized user
# Else redirects to the home page
def register_view(request):
    if not request.user.is_authenticated:
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
    return HttpResponseRedirect('/home')


# Logs out the user and redirects to the landing page
def logout_view(request):
    logout(request)
    return render(request, template_name="landing.html", context={})