from django.urls import path
from .views import create_director, director_form, create_movie, movie_form

urlpatterns = [
    path('create', create_director),
    path('createdirectorform', director_form),
    path('createmovie', create_movie),
    path('movieform/<int:director_id>', movie_form),


]
