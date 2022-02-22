from django.urls import path
from .views import *

urlpatterns = [
    path('rate/<int:movie_id>', rate_movie),
    path('user/<int:user_id>', user_reviews),
    path('search_user', search_user),
    path('movie/<int:movie_id>', movie_reviews),

]
