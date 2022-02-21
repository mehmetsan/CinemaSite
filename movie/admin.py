from django.contrib import admin
from .models import Movie, Director

# Register your models here.
admin.site.register(Director)
admin.site.register(Movie)