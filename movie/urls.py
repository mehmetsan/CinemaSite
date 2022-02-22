from django.urls import path
from .views import *

urlpatterns = [
    path('create', create_director),
    path('create_movie/<int:director_id>', create_movie),
    path('search', movie_search),
    path('detail/<int:movie_id>', movie_detail),
    path('detail/<int:movie_id>/change_watched', change_watched),
    path('movies_list', movie_list),
    path('watched_movies', watched_movies),
]
