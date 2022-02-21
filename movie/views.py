from django.shortcuts import render, HttpResponseRedirect
from .forms import CreateDirectorForm, CreateMovieForm, SearchMovie, PlatformFilter
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
    director = Director.objects.get(name=proposed_director)
    directors_movies = director.movies.all()

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
        director = Director.objects.get(id=director_id)
        director_movie_names = [each.title for each in director.movies.all()]
        if proposed_movie in director_movie_names:
            message = "Movie already present"
        else:
            message = "Movie added!"
            movie_object.director = director
            form.save()

    return render(request, template_name="result.html", context={'message': message})


def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user = request.user
    watched = False
    if movie.viewer.filter(id=user.id).exists():
        watched = True
    return render(request, template_name="detail.html", context={'movie': movie, 'watched': watched})


def movie_watched(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user = request.user
    movie.viewer.add(user)
    movie.save()
    return HttpResponseRedirect('/')


def movie_unwatched(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user = request.user
    movie.viewer.remove(user)
    movie.save()
    return HttpResponseRedirect('/')


def movie_search(request):
    form = SearchMovie(request.POST or None)
    if request.POST:
        if form.is_valid():
            title = form.cleaned_data.get('title')
            movie = Movie.objects.filter(title=title)[0]
            return HttpResponseRedirect("/movie/detail/{}".format(movie.id))

    return render(request, template_name="search_movie.html", context={'form': form})


def movie_list(request):
    all_movies = Movie.objects.all()
    user = request.user
    filter_form = PlatformFilter(request.POST or None)

    if request.POST:
        if filter_form.is_valid():
            filter_platform = filter_form.cleaned_data.get('platform')
            all_movies = all_movies.filter(platform=filter_platform)

    for movie in all_movies:
        if movie.viewer.filter(id=user.id).exists():
            movie.flag = "Watched"
        else:
            movie.flag = "Not Watched"

    return render(request, template_name="movie_list.html", context={'movies': all_movies, 'form': filter_form})


def watched_movies(request):
    user = request.user
    watched = Movie.objects.filter(viewer=user)

    filter_form = PlatformFilter(request.POST or None)

    if request.POST:
        if filter_form.is_valid():
            filter_platform = filter_form.cleaned_data.get('platform')
            watched = watched.filter(platform=filter_platform)

    return render(request, template_name="watched_movies.html", context={'movies': watched, 'form': filter_form})
