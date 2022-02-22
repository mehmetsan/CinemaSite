from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Director(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=120)
    year = models.IntegerField(blank=True,
                               validators=[MinValueValidator(1900)])
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name="movies")
    platform = models.CharField(max_length=120, null=True, blank=True)
    viewer = models.ManyToManyField(User)
    flag = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title
