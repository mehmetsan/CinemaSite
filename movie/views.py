from django.shortcuts import render, HttpResponseRedirect
from .forms import CreateDirectorForm, CreateMovieForm, SearchMovie, PlatformFilter
from .models import Director, Movie


# Used for displaying the director creation page
def create_director(request):
    form = CreateDirectorForm(request.POST or None)

    if form.is_valid():
        proposed_director = form.cleaned_data.get('name')
        result = Director.objects.filter(name__icontains=proposed_director).exists()

        if not result:
            form.save()

        director_id = Director.objects.get(name__icontains=proposed_director).id
        return HttpResponseRedirect("/movie/create_movie/{}".format(director_id))

    return render(request, template_name="create_director.html", context={'form': form})


# Used for displaying the movie creation page
# Parameter: director_id is used for referencing the correct director to match with the movie
def create_movie(request, director_id):
    director = Director.objects.get(id=director_id)
    directors_movies = director.movies.all()

    new_movie_form = CreateMovieForm(request.POST or None)
    if new_movie_form.is_valid():
        movie_object = new_movie_form.save(commit=False)
        proposed_movie = movie_object.title

        # Check whether the proposed movie already exists
        if director.movies.filter(title=proposed_movie).exists():
            message = "Movie already present"
        else:
            message = "Movie added!"
            movie_object.director = director
            movie_object.save()
        return render(request, template_name="result.html", context={"message": message})

    return render(request, template_name="create_movie.html", context={'form': new_movie_form,
                                                                       'movies': directors_movies,
                                                                       'director': director})


# Used for displaying the details page of a movie,
# Displays 'watched' flags depending on the browsing user
# Parameter: movie_id is used for referencing the correct movie
def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user = request.user
    watched = False
    if movie.viewer.filter(id=user.id).exists():
        watched = True
    return render(request, template_name="detail.html", context={'movie': movie, 'watched': watched})


# Used for changing the watched flag of a movie for the active user
# Parameter: movie_id is used for referencing the correct movie
def change_watched(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user = request.user
    if movie.viewer.filter(id=user.id).exists():
        movie.viewer.remove(user)
    else:
        movie.viewer.add(user)
    movie.save()
    return HttpResponseRedirect('/movie/movies_list')


# Used for searching a movie by its title and directing to its details page,
def movie_search(request):
    form = SearchMovie(request.POST or None)
    found = True
    if request.POST:
        if form.is_valid():
            title = form.cleaned_data.get('title')
            # Check if the movie already exists
            try:
                movie = Movie.objects.get(title=title)
                return HttpResponseRedirect("/movie/detail/{}".format(movie.id))
            except:
                found = False

    return render(request, template_name="search_movie.html", context={'form': form, 'found': found})


# Used for displaying all of the movies
# If filter is used, the display is filtered, then transferred to the view
def movie_list(request):
    all_movies = Movie.objects.all()
    user = request.user
    filter_form = PlatformFilter(request.POST or None)

    if request.POST:
        if filter_form.is_valid():
            filter_platform = filter_form.cleaned_data.get('platform')
            all_movies = all_movies.filter(platform__icontains=filter_platform)

    for movie in all_movies:
        if movie.viewer.filter(id=user.id).exists():
            movie.flag = "Watched"
        else:
            movie.flag = "Not Watched"

    return render(request, template_name="movie_list.html", context={'movies': all_movies, 'form': filter_form})


# Used for displaying the watched movie list page of the active user
# The view can be filtered
def watched_movies(request):
    user = request.user
    watched = Movie.objects.filter(viewer=user)

    filter_form = PlatformFilter(request.POST or None)

    if request.POST:
        if filter_form.is_valid():
            filter_platform = filter_form.cleaned_data.get('platform')
            watched = watched.filter(platform__icontains=filter_platform)

    return render(request, template_name="watched_movies.html", context={'movies': watched, 'form': filter_form})
