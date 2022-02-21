from django import forms
from .models import Movie, Director


class CreateDirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = '__all__'


class CreateMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ['director', 'viewer', 'flag']


class SearchMovie(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title']


class PlatformFilter(forms.Form):
    platform = forms.CharField(label="Platform name", max_length=120)
