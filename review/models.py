from django.db import models
from django.contrib.auth.models import User
from movie.models import Movie

rating_choices = [(str(each),str(each)) for each in range(0,11)]


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField()
    rating = models.CharField(max_length=2, choices=rating_choices)

    def __str__(self):
        return self.movie.title+"-"+str(self.user.id)
