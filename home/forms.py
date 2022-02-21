from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="username")
    password = forms.CharField(max_length=100, label="password", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(message="Username or Password wrong or missing")
        return super(LoginForm, self).clean()


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label="username")
    password1 = forms.CharField(max_length=100, label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label="password(again)", widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100, label="first_name")
    last_name = forms.CharField(max_length=100, label="last_name")

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")
        return password2