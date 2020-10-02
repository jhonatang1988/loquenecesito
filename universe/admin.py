from django.contrib import admin
from .models import Movie, Character, Planet, Person

# Register your models here.
admin.site.register(Movie)
admin.site.register(Character)
admin.site.register(Planet)
admin.site.register(Person)
