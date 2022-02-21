from django.forms import ModelForm
from .models import Movie, Director


class CreateDirectorForm(ModelForm):
    class Meta:
        model = Director
        fields = '__all__'


class CreateMovieForm(ModelForm):
    class Meta:
        model = Movie
        exclude = ['director']
