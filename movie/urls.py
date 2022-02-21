from django.urls import path
from .views import *

urlpatterns = [
    path('create', create_director),
    path('createdirectorform', director_form),
    path('createmovie', create_movie),
    path('movieform/<int:director_id>', movie_form),
    path('search', movie_search),
    path('detail/<int:movie_id>', movie_detail),
    path('detail/<int:movie_id>/watched', movie_watched),
    path('detail/<int:movie_id>/unwatched', movie_unwatched),
    path('movies_list', movie_list),
    path('watched_movies', watched_movies),
]
