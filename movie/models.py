from django.db import models
from django.core.validators import MinValueValidator


class Director(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=120)
    year = models.IntegerField(default=1900,
                               blank=True,
                               validators=[MinValueValidator(1900)])
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name="movies")

    def __str__(self):
        return self.title
