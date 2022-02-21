from django.shortcuts import render
from .forms import CreateDirectorForm, CreateMovieForm
from .models import Director, Movie


# Create your views here.
def create_director(request):
    form = CreateDirectorForm()
    return render(request, template_name="create_director.html", context={'form': form})


def director_form(request):
    form = CreateDirectorForm(request.POST)
    directors_movies, message = "", ""

    if form.is_valid():
        proposed_director = form.cleaned_data.get('name')
        print("Proposed name: ", proposed_director)
        result = Director.objects.filter(name=proposed_director)

        if not result:
            form.save()
            message = "Director created"
        else:
            message = "Director already present"

    new_movie_form = CreateMovieForm()
    director = Director.objects.filter(name=proposed_director)[0]
    directors_movies = director.movies.all()

    print(directors_movies)
    return render(request, template_name="create_movie.html", context={'message': message, "form": new_movie_form,
                                                                       'movies': directors_movies,
                                                                       'director': director})


def create_movie(request):
    return render(request, template_name="create_movie.html", context={})


def movie_form(request, director_id):
    form = CreateMovieForm(request.POST)

    if form.is_valid():
        movie_object = form.save(commit=False)
        proposed_movie = form.cleaned_data.get('title')
        director = Director.objects.filter(id=director_id)[0]
        director_movie_names = [each.title for each in director.movies.all()]
        if proposed_movie in director_movie_names:
            message = "Movie already present"
        else:
            message = "Movie added!"
            movie_object.director = director
            form.save()

    return render(request, template_name="result.html", context={'message': message})